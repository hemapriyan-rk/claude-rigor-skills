# Where to get timing data

## Pipelines

| CI | Command or source |
|---|---|
| **GitHub Actions** | `gh run list --workflow <file> --limit 20 --json databaseId,createdAt,updatedAt,conclusion` for run durations; `gh api repos/<owner>/<repo>/actions/runs/<run_id>/jobs` for per-job and per-step `started_at` / `completed_at` |
| **GitLab CI** | `GET /projects/:id/pipelines/:pipeline_id/jobs` (each job has `duration` and `queued_duration`); the pipeline graph view for dependencies |
| **CircleCI** | Insights API: `/insights/{project-slug}/workflows/{workflow}/jobs` |
| **Jenkins** | Pipeline Stage View, or the `wfapi/describe` endpoint per build |
| **Any** | Timestamps in the raw logs; wrap steps with `time` |

Count queue time separately from run time. Long queues mean too few runners, not slow jobs.

## Tests

| Runner | How to get per-test timing |
|---|---|
| **pytest** | `pytest --durations=0 -q` (add `--durations-min=0.1` to cut noise); `--junitxml=report.xml` |
| **Jest / Vitest** | `jest --verbose`, or a JUnit reporter (`jest-junit`); Vitest `--reporter=verbose` |
| **Go** | `go test -json ./... ` and read the `Elapsed` fields; `-v` prints per-test times |
| **JUnit / Maven / Gradle** | Surefire reports in `target/surefire-reports`; Gradle `build/reports/tests` |
| **RSpec** | `rspec --profile 20` |

## Setup costs to time separately

- Dependency install (`npm ci`, `pip install`, `go mod download`, Maven/Gradle resolution).
- Container image pull and service containers (databases, queues).
- Per-test fixtures: database creation and migrations, app startup, browser launch.
- Compilation and asset builds.

## Comparing before and after

- Same commit, same runner type, at least 3 runs each; compare medians.
- For local test suites, run each version 3 times and report the median and spread.
- A change smaller than the run-to-run spread isn't a measured saving.
