"""OpenAI Responses API client using only the Python standard library."""

from __future__ import annotations

import json
import urllib.error
import urllib.request


class OpenAIError(RuntimeError):
    """Raised when the OpenAI request fails or returns an unexpected shape."""


def create_response(
    *,
    api_key: str,
    model: str,
    instructions: str,
    user_input: str,
    api_base: str = "https://api.openai.com/v1",
    max_output_tokens: int = 1800,
) -> str:
    if not api_key:
        raise OpenAIError("OPENAI_API_KEY is required")

    url = f"{api_base.rstrip('/')}/responses"
    payload = {
        "model": model,
        "instructions": instructions,
        "input": user_input,
        "max_output_tokens": max_output_tokens,
    }
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise OpenAIError(f"OpenAI API returned {exc.code}: {detail}") from exc
    except OSError as exc:
        raise OpenAIError(f"Failed to call OpenAI API: {exc}") from exc

    text = extract_output_text(data)
    if not text:
        raise OpenAIError("OpenAI response did not contain output text")
    return text


def extract_output_text(data: dict) -> str:
    output_text = data.get("output_text")
    if isinstance(output_text, str):
        return output_text

    parts: list[str] = []
    for item in data.get("output", []):
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"}:
                text = content.get("text")
                if isinstance(text, str):
                    parts.append(text)
    return "\n".join(parts).strip()
