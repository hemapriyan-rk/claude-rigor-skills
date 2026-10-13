# Profilers and benchmark methods

Use the row for the language or layer in front of you.

## By runtime

| Runtime | CPU profile | Wall-clock / I-O | Memory | Quick timing |
|---|---|---|---|---|
| **Python** | `python -m cProfile -s cumtime script.py` | `py-spy record -o out.svg -- python script.py` (sampling, includes waits) | `tracemalloc`, `memray run script.py` | `python -m timeit`, `time.perf_counter()` |
| **Node.js** | `node --cpu-prof app.js` (open `.cpuprofile` in Chrome DevTools) | `clinic doctor -- node app.js`, `clinic bubbleprof` | `node --heap-prof`, heap snapshots in DevTools | `console.time`, `performance.now()` |
| **Go** | `go test -cpuprofile cpu.out -bench .`, then `go tool pprof cpu.out` | `net/http/pprof` endpoint, `go tool trace` | `-memprofile mem.out`, `pprof -alloc_space` | `go test -bench . -benchmem` |
| **Java / JVM** | async-profiler (`asprof -d 30 -f out.html <pid>`) | Java Flight Recorder (`-XX:StartFlightRecording`) | JFR allocation events, heap dumps | JMH for microbenchmarks |
| **Rust** | `cargo flamegraph`, `perf record` | `tokio-console` for async | `heaptrack`, `dhat` | `criterion` |
| **C / C++** | `perf record -g` + `perf report`, Callgrind | `perf` off-CPU analysis | Massif, `heaptrack` | Google Benchmark |
| **.NET** | `dotnet-trace collect` | `dotnet-counters` | `dotnet-gcdump` | BenchmarkDotNet |

## By layer

| Layer | Tool |
|---|---|
| **SQL** | `EXPLAIN ANALYZE` (Postgres), `EXPLAIN FORMAT=JSON` (MySQL). Look for sequential scans on large tables, nested loops over many rows, and row-estimate errors. Count queries per request to find N+1 patterns |
| **HTTP service** | Load test with `k6`, `wrk`, or `hey`. Report p50/p95/p99, not the average |
| **Browser** | DevTools Performance panel, Lighthouse, Web Vitals (LCP, INP, CLS) |
| **Whole system** | Distributed traces: find the span that dominates end-to-end time before profiling any single service |

## Benchmark hygiene

- Warm up before measuring (JIT, caches, connection pools).
- Run at least 5 repetitions and report the median and spread. A change smaller than the run-to-run spread isn't a measured improvement.
- Use realistic input size and shape. Small inputs hide superlinear algorithms.
- Change one thing at a time between measurements.
- Measure on the same machine and with the same load, or the comparison doesn't mean anything.
