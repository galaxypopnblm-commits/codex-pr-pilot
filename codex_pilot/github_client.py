"""Small GitHub REST client."""

from __future__ import annotations

import json
import urllib.error
import urllib.request


class GitHubError(RuntimeError):
    """Raised when GitHub rejects a request."""


def create_issue_comment(
    *,
    repo: str,
    issue_number: int,
    body: str,
    token: str,
    api_url: str = "https://api.github.com",
) -> str:
    if not repo or "/" not in repo:
        raise GitHubError("repo must look like owner/name")
    if not token:
        raise GitHubError("GITHUB_TOKEN is required to post a comment")

    url = f"{api_url.rstrip('/')}/repos/{repo}/issues/{issue_number}/comments"
    payload = json.dumps({"body": body}).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=payload,
        method="POST",
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "codex-pr-pilot",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise GitHubError(f"GitHub API returned {exc.code}: {detail}") from exc
    except OSError as exc:
        raise GitHubError(f"Failed to call GitHub API: {exc}") from exc

    return str(data.get("html_url") or "")
