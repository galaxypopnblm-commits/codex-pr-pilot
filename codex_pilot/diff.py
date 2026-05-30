"""Diff collection helpers."""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from typing import Optional


class DiffError(RuntimeError):
    """Raised when a diff cannot be collected."""


def read_diff_file(path: str | os.PathLike[str]) -> str:
    diff_path = Path(path)
    try:
        return diff_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise DiffError(f"Failed to read diff file {diff_path}: {exc}") from exc


def run_git_diff(base: str, head: str, cwd: Optional[str] = None) -> str:
    command = ["git", "diff", "--no-ext-diff", "--unified=80", base, head]
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        detail = getattr(exc, "stderr", "") or str(exc)
        raise DiffError(f"Failed to run git diff {base}..{head}: {detail.strip()}") from exc
    return result.stdout


def pull_request_number(event_path: Optional[str] = None) -> Optional[int]:
    path = event_path or os.getenv("GITHUB_EVENT_PATH")
    if not path:
        return None
    try:
        event = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    pull_request = event.get("pull_request") or {}
    number = pull_request.get("number") or event.get("number")
    try:
        return int(number)
    except (TypeError, ValueError):
        return None
