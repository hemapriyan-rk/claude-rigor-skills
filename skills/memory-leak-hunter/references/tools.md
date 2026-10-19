# Tools by runtime

| Runtime | Heap measure for the growth test | Snapshot and diff | Find who holds it |
|---|---|---|---|
| **Python** | `gc.collect()` then `tracemalloc.get_traced_memory()[0]`; process RSS via `psutil` | `tracemalloc.take_snapshot()` at two checkpoints, then `snap2.compare_to(snap1, "lineno")` (or `"traceback"`) | `gc.get_referrers(obj)`, `objgraph.show_growth()`, `objgraph.show_backrefs()` |
| **Node.js** | Run with `--expose-gc`; call `global.gc()` then `process.memoryUsage().heapUsed` | `v8.writeHeapSnapshot()` at two checkpoints; open both in Chrome DevTools → Memory → Comparison | Retainers panel in DevTools; `--heapsnapshot-signal=SIGUSR2` for running servers |
| **Java / JVM** | `jcmd <pid> GC.run` then `jcmd <pid> GC.heap_info`, or used heap from JFR | `jcmd <pid> GC.class_histogram` twice and diff; heap dumps with `jcmd <pid> GC.heap_dump` | Eclipse MAT dominator tree and "path to GC roots"; JFR `OldObjectSample` events |
| **Go** | `runtime.GC()` then `runtime.ReadMemStats` → `HeapInuse`; `runtime.NumGoroutine()` | `go tool pprof -inuse_space` on two heap profiles; `-base` to diff | `pprof` `list` / `peek` on the growing allocation site; goroutine profile for blocked goroutines |
| **C / C++ / Rust** | Allocator stats or RSS | `heaptrack`, Massif, `valgrind --leak-check=full` | Allocation call stacks in those tools |

## Growth test template (Python)

```python
import gc, tracemalloc

def run(n):
    for _ in range(n):
        handle_one_request()      # the unit of work

tracemalloc.start(25)
run(1000); gc.collect(); base = tracemalloc.take_snapshot()
for checkpoint in (1000, 2000, 4000):
    run(checkpoint); gc.collect()
    print(checkpoint, tracemalloc.get_traced_memory()[0])
diff = tracemalloc.take_snapshot().compare_to(base, "lineno")
for stat in diff[:10]:
    print(stat)
```

Warm up first (the first run loads modules and fills caches), then measure.

## Reading the curve

| Shape | Meaning |
|---|---|
| Straight line up with iterations | Leak: something is kept per unit of work |
| Rises then flat | Cache, pool or JIT warming up. Check that it has a size limit |
| Steps up occasionally, never down | Often a growing array or hash table resizing. Still a leak if it never shrinks and keeps growing |
| Heap flat, RSS up | Fragmentation or native memory (C extensions, buffers, off-heap) |
