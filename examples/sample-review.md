## Summary

The diff adds a small `app.py` module with an environment-backed API key reader and an `add` helper.

## Review notes

- `read_api_key()` raises `KeyError` when `OPENAI_API_KEY` is missing. That may be fine for a CLI fail-fast path, but callers should either document it or convert it into a clearer error.
- No secret value is hardcoded in the diff.

## Test suggestions

- Add a test for `add(1, 2)`.
- Add tests for `read_api_key()` with the environment variable present and absent.

## Maintainer checklist

- [ ] Decide whether missing environment variables should raise `KeyError` or a custom error.
- [ ] Add unit tests for the new helpers.
