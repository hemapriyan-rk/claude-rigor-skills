# Common leak patterns

| Pattern | What it looks like | Fix |
|---|---|---|
| **Listener never removed** | `bus.subscribe(handler)`, `emitter.on(...)`, `addEventListener` per request or per component, with no matching unsubscribe | Unsubscribe in `finally` or on teardown; use `once`; scope the bus to the request |
| **Unbounded cache or memo** | Module-level `dict` or `Map` keyed by request ID, user ID, or timestamp; `@lru_cache(maxsize=None)` on functions taking unique arguments | Size limit with eviction (LRU, TTL); key by something with bounded cardinality |
| **Closure captures a large object** | A callback or lambda stored long-term that references a request, response, buffer or DataFrame | Capture only the fields needed; clear the reference after use |
| **Growing collection on a long-lived object** | `self.history.append(...)`, a log list, an "all results" list on a singleton or service | Cap it, rotate it, or stream it out |
| **Resources not closed** | Files, sockets, DB cursors, HTTP responses, subprocess pipes without `with` / `try-finally` / `defer` | Context managers, `try/finally`, `defer Close()` |
| **Thread-local or context leftovers** | Thread pools reuse threads; values set in thread-local storage are never cleared | Clear at the end of each task |
| **Goroutine or task never ends** | Blocked on a channel nobody writes to, or a missing `ctx.Done()` case; `asyncio` tasks never awaited | Cancellation through context; close channels; track and await tasks |
| **Timers and intervals** | `setInterval` or scheduled jobs created per request and never cleared | Clear on teardown; create once |
| **Global registries** | Plugin, class or handler registries that are appended to at runtime | Register once at startup; dedupe |
| **Reference cycles with finalizers** (older Python, some C extensions) | Objects with `__del__` in cycles | Break the cycle explicitly, or use `weakref` |
| **Detached DOM nodes** (browser) | Removed elements still referenced from JS arrays, maps or closures | Drop references when removing elements |

## Not leaks (don't "fix" these)

- A cache that grows to its configured limit and stays there.
- The first run of a JIT or interpreter loading code and data.
- Memory a garbage collector hasn't returned to the OS yet, when the heap itself is flat.
