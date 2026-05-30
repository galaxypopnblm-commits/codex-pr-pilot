"""Command-line entry point for Codex PR Pilot."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from .diff import DiffError, pull_request_number, read_diff_file, run_git_diff
from .github_client import GitHubError, create_issue_comment
from .openai_client import OpenAIError, create_response
from .review import SYSTEM_INSTRUCTIONS, build_user_prompt, render_dry_run_review, trim_diff


DEFAULT_MODEL = "gpt-5.4-mini"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate an AI-assisted pull request review from a git diff."
    )
    parser.add_argument("--diff-file", help="Read diff content from a file instead of git.")
    parser.add_argument("--base", default=os.getenv("CODEX_PILOT_BASE", "HEAD~1"))
    parser.add_argument("--head", default=os.getenv("CODEX_PILOT_HEAD", "HEAD"))
    parser.add_argument("--model", default=os.getenv("OPENAI_MODEL", DEFAULT_MODEL))
    parser.add_argument("--api-base", default=os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1"))
    parser.add_argument("--max-diff-chars", type=int, default=60000)
    parser.add_argument("--max-output-tokens", type=int, default=1800)
    parser.add_argument("--dry-run", action="store_true", help="Do not call OpenAI or GitHub.")
    parser.add_argument("--output", help="Write review Markdown to this file.")
    parser.add_argument("--comment", action="store_true", help="Post the review as a PR comment.")
    parser.add_argument("--repo", default=os.getenv("GITHUB_REPOSITORY"))
    parser.add_argument("--pr-number", type=int, default=pull_request_number())
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    try:
        diff = read_diff_file(args.diff_file) if args.diff_file else run_git_diff(args.base, args.head)
    except DiffError as exc:
        print(f"codex-pilot: {exc}", file=sys.stderr)
        return 2

    if not diff.strip():
        print("codex-pilot: no diff content found; skipping review.")
        return 0

    trimmed_diff, truncated = trim_diff(diff, args.max_diff_chars)
    if args.dry_run:
        review = render_dry_run_review(trimmed_diff, truncated=truncated)
    else:
        try:
            review = create_response(
                api_key=os.getenv("OPENAI_API_KEY", ""),
                api_base=args.api_base,
                model=args.model,
                instructions=SYSTEM_INSTRUCTIONS,
                user_input=build_user_prompt(trimmed_diff),
                max_output_tokens=args.max_output_tokens,
            )
        except OpenAIError as exc:
            print(f"codex-pilot: {exc}", file=sys.stderr)
            return 3

    print(review)
    write_output(review, args.output)
    write_step_summary(review)

    if args.comment and not args.dry_run:
        try:
            url = create_issue_comment(
                repo=args.repo or "",
                issue_number=int(args.pr_number or 0),
                body=review,
                token=os.getenv("GITHUB_TOKEN", ""),
            )
        except (GitHubError, ValueError) as exc:
            print(f"codex-pilot: failed to post PR comment: {exc}", file=sys.stderr)
            return 4
        if url:
            print(f"codex-pilot: posted PR comment: {url}")

    return 0


def write_output(review: str, output: str | None) -> None:
    if output:
        Path(output).write_text(review, encoding="utf-8")


def write_step_summary(review: str) -> None:
    summary_path = os.getenv("GITHUB_STEP_SUMMARY")
    if summary_path:
        with open(summary_path, "a", encoding="utf-8") as handle:
            handle.write(review)
            handle.write("\n")


if __name__ == "__main__":
    raise SystemExit(main())
