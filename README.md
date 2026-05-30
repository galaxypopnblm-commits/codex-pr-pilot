# Codex PR Pilot

[![CI](https://github.com/galaxypopnblm-commits/codex-pr-pilot/actions/workflows/ci.yml/badge.svg)](https://github.com/galaxypopnblm-commits/codex-pr-pilot/actions/workflows/ci.yml)

Codex PR Pilot is a lightweight GitHub Actions assistant for pull request maintainers. It reads a PR diff, asks an OpenAI model for a focused review, and can post the result back as a pull request comment.

The first version is intentionally small:

- summarize what changed
- flag review risks and follow-up questions
- suggest tests that would make the PR safer to merge
- run locally with a diff file or inside GitHub Actions

It does not approve, reject, or modify pull requests.

## Quick Start

Install from a checkout:

```bash
pip install -e .
```

Run a local dry-run without calling any API:

```bash
codex-pilot --diff-file examples/sample.diff --dry-run
```

Run with OpenAI:

```bash
export OPENAI_API_KEY="sk-..."
codex-pilot --diff-file examples/sample.diff
```

The default model is `gpt-5.4-mini`. Override it with:

```bash
codex-pilot --model gpt-5.5 --diff-file examples/sample.diff
```

## GitHub Actions

Add `OPENAI_API_KEY` as a repository secret, then use:

```yaml
name: Codex PR Pilot

on:
  pull_request:
    types: [opened, synchronize, reopened]

permissions:
  contents: read
  issues: write
  pull-requests: read

jobs:
  review:
    runs-on: ubuntu-latest
    env:
      OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
      GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - run: pip install .

      - name: Review PR
        if: env.OPENAI_API_KEY != ''
        run: >
          codex-pilot
          --base "${{ github.event.pull_request.base.sha }}"
          --head "${{ github.sha }}"
          --comment
```

## Local Development

```bash
python -m unittest discover -s tests
python -m codex_pilot.cli --diff-file examples/sample.diff --dry-run
```

## Roadmap

- update an existing bot comment instead of creating a new one each run
- add structured output mode for machine-readable review sections
- support path filters and max-diff policies
- add a reusable GitHub Action wrapper

## License

MIT
