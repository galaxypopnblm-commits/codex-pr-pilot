"""Prompt and review rendering logic."""

from __future__ import annotations


SYSTEM_INSTRUCTIONS = """You are Codex PR Pilot, a careful assistant for open source maintainers.
Review only the provided git diff.
Be specific, conservative, and concise.
Do not claim certainty for issues that are only possible risks.
Return Markdown with these sections:
1. Summary
2. Review notes
3. Test suggestions
4. Maintainer checklist
"""


def build_user_prompt(diff: str) -> str:
    return f"""Please review this pull request diff.

Focus on:
- behavior changes
- correctness risks
- security or secret-handling risks
- missing tests
- small follow-up questions for the maintainer

```diff
{diff}
```
"""


def trim_diff(diff: str, max_chars: int) -> tuple[str, bool]:
    if len(diff) <= max_chars:
        return diff, False
    return diff[:max_chars] + "\n\n[Diff truncated by Codex PR Pilot]\n", True


def render_dry_run_review(diff: str, *, truncated: bool = False) -> str:
    changed_files = []
    for line in diff.splitlines():
        if line.startswith("diff --git "):
            changed_files.append(line.rsplit(" ", 1)[-1].removeprefix("b/"))

    files = "\n".join(f"- `{name}`" for name in changed_files) or "- No files detected"
    note = "\n\n> Diff was truncated before review." if truncated else ""
    return f"""## Summary

Dry-run mode parsed the diff successfully.

Changed files:
{files}

## Review notes

No model call was made because `--dry-run` was used.

## Test suggestions

Run without `--dry-run` and with `OPENAI_API_KEY` set to generate model-backed suggestions.

## Maintainer checklist

- [ ] Confirm the diff source is correct.
- [ ] Add `OPENAI_API_KEY` before enabling live reviews.
- [ ] Use `--comment` only in trusted GitHub Actions contexts.{note}
"""
