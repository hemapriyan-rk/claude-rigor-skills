---
name: ci-speedup
description: Make slow CI pipelines and test suites faster with evidence. Times every job, step and test from real runs, fixes the biggest costs first (wasted runs, missing caches, serial jobs, slow tests), and compares time to green before and after. GitHub Actions, GitLab CI, pytest, Jest, Go, JUnit.
---

# CI Speedup

Developers wait on CI dozens of times a day, so minutes there cost more than almost anywhere else. Tweaking whatever job looks heavy usually misses the real cost. Time the pipeline, find the longest chain, cut the biggest items on it, and compare the same measurement after.

## 1. Set scope and budget

- **Agree on the metric:** usually wall-clock time from push to all required checks green on a pull request. Use the median of recent runs, not one run.
- **Read the references with the config.** In the same step as the CI config and test setup, read `references/timing-sources.md` and `references/levers.md` from this skill's base directory.
- **Don't trade correctness for speed.** Never drop required checks, hide failures behind a cache, or add blind retries for flaky tests.

## 2. Measure

- **Pipeline:** per-job and per-step durations from recent runs (see the timing sources). Note which jobs run in parallel and which wait on others.
- **Tests:** per-test durations from the runner (`pytest --durations=0`, `jest --verbose`, `go test -v -json`, JUnit XML). Also time setup: dependency install, fixtures, database creation, container start.
- **Critical path:** the longest chain of dependent jobs. Only time on that path changes how long developers wait. Speeding up a job off the path saves compute but no wall-clock time.
- If you can't access CI logs, measure locally what you can (the test suite, the build) and give the user the commands for the rest. Label anything not measured as an estimate.

## 3. Fix in order of leverage

1. **Don't run what isn't needed:** path filters (docs-only changes skip the build), cancel superseded runs on the same branch, don't rebuild what an earlier job already built.
2. **Cache:** dependencies keyed on the lockfile hash, build outputs, Docker layers. Check the cache actually hits.
3. **Parallelize the critical path:** split independent jobs, use a matrix, shard tests by timing data rather than by file count.
4. **Speed up slow tests:** replace sleeps with waiting on a condition, share expensive fixtures safely (session scope, transaction rollback instead of recreating the database), stub real network calls, run CPU-bound suites in parallel workers (`pytest -n`, Jest workers).
5. **Smaller images and runners:** slimmer base images, preinstalled tools, bigger runners only for jobs on the critical path.

Each change needs its own measured saving. Drop changes that don't move the metric.

## 4. Verify

- Re-run the same measurement on the same commit: the test suite locally, or the pipeline at least three times, compared by median.
- Confirm the same tests ran and passed (same count, same results). A faster suite that silently skips tests is a regression.
- Confirm the caches hit on the second run and that a lockfile change correctly misses.

## Output

```
## Result
Time to green: <before> → <after> (median of <n> runs). Tests: <count> before and after, all passing.

## Where the time went
| Job / step / test | Before | After | On critical path? |

## Changes
<each change, its measured saving, and the config or code diff>.

## Not changed, and why
<items considered but skipped: off the critical path, too risky, not measurable here>.
```

For example: *"Time to green: 14m 10s → 6m 05s (median of 3). The e2e job waited on a serial build job it didn't need; `npm ci` ran without a cache in 4 jobs (2m 20s each)."*
