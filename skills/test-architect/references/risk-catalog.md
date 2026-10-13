# Risk catalog

Pick the rows for the dependencies and inputs the code actually has.

## Failures by dependency type

| Dependency | Cases to test |
|---|---|
| **HTTP / RPC call** | Timeout; connection refused; 5xx; 429 with `Retry-After`; 4xx the code doesn't expect; 200 with a malformed or truncated body; very slow response; redirect loop |
| **Database** | Connection dropped mid-transaction; unique or foreign-key constraint violation; deadlock or serialization failure (should retry); empty result vs. `null`; the same row updated concurrently |
| **Filesystem** | File missing; permission denied; disk full during write; partial write then crash; path with spaces, unicode, or `..`; file changed between check and use |
| **Queue / stream** | Same message delivered twice; messages out of order; poison message that always fails; consumer crash after processing but before ack |
| **Cache** | Miss; stale value after a write; cache unavailable (should fall back, not fail) |
| **Clock / time** | Time zones and DST transitions; midnight and month boundaries; leap day; clock going backwards; expiry exactly at the boundary |
| **Randomness** | Seed it in tests; check the edge values the generator can return |
| **Environment / config** | Variable missing; set but empty; wrong type ("yes" vs `true`) |
| **ML model** | Out-of-distribution input; empty or oversized input; low-confidence output takes the fallback path; model unavailable |

## Input boundaries

| Input type | Values to try |
|---|---|
| **Numbers** | 0, 1, -1, max, max + 1, NaN, infinity, float precision (0.1 + 0.2) |
| **Strings** | Empty, whitespace only, very long, unicode and emoji, mixed normalization (é as one or two code points), embedded null byte |
| **Collections** | Empty, one item, duplicates, unsorted, very large |
| **Money** | Zero, negative, sub-cent amounts, rounding at .5, currency mismatch |
| **Dates** | See Clock / time above |
| **Identifiers** | Non-existent, belonging to another user, malformed |

## Concurrency techniques

| Language | How to test it |
|---|---|
| **Python** | Run the operation from many threads with `concurrent.futures`, start them together with a `threading.Barrier`, then assert on the final state |
| **JavaScript** | `Promise.all` over many concurrent calls; check for interleaving at every `await` |
| **Go** | `go test -race`; many goroutines started together with a `sync.WaitGroup` |
| **Java** | `ExecutorService` with a `CountDownLatch` start gate; jcstress for low-level races |
| **Database** | Two connections in separate transactions changing the same row |

## Property-based testing

| Language | Library |
|---|---|
| Python | Hypothesis |
| JavaScript / TypeScript | fast-check |
| Go | `testing/quick`, rapid |
| Java | jqwik |
| Rust | proptest |

Good properties to test: round-trip (`decode(encode(x)) == x`), idempotence (`f(f(x)) == f(x)`), invariants (a total never goes negative), and agreement with a simpler reference implementation.
