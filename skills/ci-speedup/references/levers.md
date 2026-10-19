# Levers, with config snippets

## Skip work that isn't needed

GitHub Actions: skip docs-only changes and cancel superseded runs.

```yaml
on:
  pull_request:
    paths-ignore: ["docs/**", "**/*.md"]
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

GitLab CI: `rules: - changes: [src/**/*]` on jobs, and `interruptible: true` with auto-cancel of redundant pipelines.

If a required check is skipped by a path filter, branch protection may wait forever. Use a lightweight job that always reports, or the CI's built-in handling for skipped required checks.

## Cache dependencies and builds

```yaml
- uses: actions/setup-node@v4
  with: { node-version: 20, cache: npm }        # keyed on package-lock.json
- uses: actions/setup-python@v5
  with: { python-version: "3.12", cache: pip }  # keyed on requirements files
```

General `actions/cache`: key on the lockfile hash, e.g. `key: deps-${{ runner.os }}-${{ hashFiles('**/poetry.lock') }}`.
GitLab: `cache: key: files: [package-lock.json]`.
Docker: `docker/build-push-action` with `cache-from: type=gha` and `cache-to: type=gha,mode=max`.

Check the logs for "Cache restored" on the second run.

## Parallelize

- **Split independent jobs:** lint, type-check, unit tests and build don't need to wait on each other. Only add `needs:` (GitHub Actions and GitLab) for real dependencies.
- **Matrix only what you must:** every matrix entry is a full job. Run the full OS/version matrix on main or nightly, a single entry on pull requests, if the team accepts that.
- **Shard tests by timing:** `pytest-split --splits N --group i` (uses stored durations), Jest `--shard=i/N`, `go test` packages across jobs. Sharding by file count leaves one slow shard.
- **Parallel workers in one job:** `pytest -n auto` (pytest-xdist), Jest workers, `go test -p`. Tests must not share mutable state (ports, files, database rows).

## Slow tests

| Cause | Fix |
|---|---|
| `time.sleep` / `setTimeout` waiting for something | Poll for the condition with a timeout, or use a fake clock |
| Database created and migrated per test | Create once per session; wrap each test in a transaction and roll back |
| Real HTTP calls to third parties | Stub at the client boundary (responses, nock, httptest) |
| App or browser started per test | Start once per module or session, reset state between tests |
| Large fixtures loaded per test | Load once, copy only if tests mutate them |
| Retries hiding flaky failures | Fix or quarantine the flaky test; don't retry by default |

## Runners and images

- Preinstall tools in a custom image instead of installing them every run.
- Prefer slim base images; pull service containers only in jobs that need them.
- Bigger runners pay off only for CPU-bound jobs on the critical path.
