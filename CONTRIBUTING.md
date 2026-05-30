# Contributing

Thanks for taking a look at Codex PR Pilot. This project is young, so small, focused contributions are the most useful right now.

## Good First Contributions

- improve README examples
- add tests around diff parsing and CLI flags
- add GitHub Actions examples for common repository layouts
- improve error messages for missing environment variables

## Development Setup

```bash
pip install -e .
python -m unittest discover -s tests
codex-pilot --diff-file examples/sample.diff --dry-run
```

## Pull Request Guidelines

- Keep PRs focused on one behavior or documentation change.
- Add or update tests when behavior changes.
- Use dry-run mode when demonstrating CLI output without making API calls.
- Avoid including secrets, private repository diffs, or sensitive code in examples.

## Project Boundaries

Codex PR Pilot should help maintainers review changes. It should not automatically approve, reject, or modify pull requests.
