# Demo: `ci-speedup` on a small Python project

Run on 2026-10-19 in a fresh, headless Claude Code session (model `claude-sonnet-5-5`, `--setting-sources project,local` so only this skill was installed) in a copy of the [`before/`](before/) project with the skill. [output.md](output.md) is the session's output, unedited.

## Prompt

```text
Use the ci-speedup skill on this repo. Our GitHub Actions CI takes about 12 minutes per pull request, and the test suite is slow locally too. Make it faster without dropping any checks.
```

**Tools allowed:** Skill, Read, Edit, Write, Glob, Grep, `python`, `pytest`. **Cost:** $0.20, 71 seconds.

## Files

- [`before/`](before/) is the project the session was given: a serial `lint → test → build` workflow with no caching, a 40,000-row fixture rebuilt for every test, and notifier tests that `sleep` for fixed times.
- [`after/`](after/) holds only the three files the session changed: `.github/workflows/ci.yml`, `tests/conftest.py`, and `tests/test_notifier.py`.

## What to look for

- It measured per-test durations before changing anything, and fixed the two biggest costs: fixed sleeps (replaced by waiting on the queue) and the per-test fixture (now loaded once per session).
- **Checked independently:** the test suite went from 8.85 s to 0.43 s, with the same 17 tests passing. The new workflow is valid YAML and still runs lint, the full 3.10/3.11/3.12 matrix, and build.
- It labelled the CI time savings as estimates, because no GitHub run history was available, and told you how to confirm them after pushing.
- It disclosed one behaviour change: `push` now triggers only on `main`, because pushes to pull-request branches ran every job twice.

## Run it yourself

```sh
cp -r before /tmp/ci-demo && cd /tmp/ci-demo
python -m pytest -q                         # ~9 s
cp -r <repo>/examples/ci-speedup/after/. .
python -m pytest -q                         # ~0.4 s
```

Model output varies from run to run, so a re-run will be worded differently.
