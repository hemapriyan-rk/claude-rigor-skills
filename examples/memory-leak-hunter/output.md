## Result
Growth: about 11.5 KB per message at 1k messages, rising to 31.7 KB per message at 4k, then 0 B per message. The "after" run covered 8,000 messages. The "before" run died with `MemoryError` at about 4.5k messages. Behaviour is unchanged. I ran 2,000 simulated messages and every response still reports `audit_events == 1` and the same `ok`/`rejected` statuses. I did not run a before/after diff of full outputs or any project tests, since none exist here.

## Cause
`handle_message` calls `bus.subscribe("audit", record_audit)` on the module-level `bus` for every message and never unsubscribes (`worker.py:45`). The retaining chain is `bus._handlers["audit"]` → `record_audit` closure → `ctx` (`RequestContext`) → `ctx.raw` (the JSON of the whole message, up to 2 KB) and `ctx.audit_log`.

The audit handler count grew by exactly one per message: 1,500, then 2,500, then 4,500 at the checkpoints. Growth also sped up, because every leaked handler receives every later audit event and appends it to its own `audit_log`. That makes the leak quadratic in memory and CPU, which fits the slow climb to OOM in production.

## Change
`worker.py` now wraps the body in `try/finally` and calls `bus.unsubscribe("audit", record_audit)` in the `finally` block. This cuts the root reference, so each `ctx` is freed when its message finishes. The `finally` also covers the early `rejected` return and any exception. The audit handler list is empty after the run.

I added `growth_test.py`, which is the repeatable growth test (tracemalloc, with a `gc.collect()` at each checkpoint). Delete it if you don't want it in the repo.

## Remaining risk
- `tax_rate` uses `lru_cache(maxsize=512)` and is keyed by country, so it is bounded and not a leak.
- This only tests the simulated workload. The real queue consumer may have other leaks, such as connection handling, that `simulate.py` doesn't reach. I didn't measure RSS or native memory.
- `bus` is a global singleton. Any other code that subscribes per call has the same problem. Scoping the bus to the request would remove that whole class of bug, but it is a bigger change than this fix needs.