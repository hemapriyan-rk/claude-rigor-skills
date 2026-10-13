# Failure modes and threats by component

Check each component in the design against its row. Skip rows that don't apply.

## Failure modes

| Component | Failure modes to check | Typical mitigations |
|---|---|---|
| **Relational database** | Primary down; failover takes 30–120 s; replica lag serves stale reads; connection pool exhausted; lock contention or long transactions; disk full; a slow query takes the whole pool | Read-your-writes routing, pool limits and timeouts, statement timeouts, separate pools for slow jobs, tested failover |
| **Key-value cache** | Cold start after restart; stampede when a hot key expires; stale data after a write; eviction under memory pressure; cache down means full load hits the database | Request coalescing, jittered TTLs, write-through or explicit invalidation, load shedding when the cache is down |
| **Message queue / stream** | Consumer lag grows without bound; duplicate delivery (at-least-once); out-of-order delivery across partitions; poison message blocks a partition; retention expires before consumers catch up | Idempotent consumers, dead-letter queue, partition by the key that needs ordering, lag alerts |
| **Synchronous service call** | Timeout; slow response holds threads; retries multiply load (retry storm); partial success | Timeouts below the caller's own deadline, retry budget with backoff and jitter, circuit breaker, idempotency keys |
| **Load balancer / gateway** | Health check passes while the app is broken; uneven load; connection limits; TLS certificate expiry | Deep health checks, least-connections routing, certificate expiry alerts |
| **Object storage** | Eventual listing after write; request-rate limits per prefix; accidental public access; lifecycle rules deleting live data | Write-then-read by key, spread prefixes, block public access by default |
| **Third-party API** | Outage; rate limits; schema change; slow responses; price change | Timeouts, cached fallback, contract tests, a second provider for critical paths |
| **Scheduled / batch job** | Overlapping runs; partial run leaves inconsistent state; silently stops running | Locking, idempotent and resumable steps, alert on "hasn't run" |
| **ML model service** | Out-of-distribution input with confident wrong output; latency spike on large input; model and feature versions out of sync; drift over time | Confidence threshold with a defined fallback, input size limits, versioned features, drift monitoring |
| **Edge device** | Loses connectivity for hours; clock drift; storage fills while offline; power loss mid-write; firmware update fails | Local queue with a cap, server-side timestamps, atomic writes, A/B firmware partitions |
| **Agent / LLM step** | Loops without terminating; cost runaway; prompt injection through tool output; non-deterministic output breaks a parser | Step and cost caps, tool allow-list, treat tool output as data, schema-validated output with retry |

## Threats by boundary

| Boundary | What to check |
|---|---|
| **Public API** | Authentication on every route, authorization per object (IDOR), rate limits, input size limits, injection |
| **Service to service** | Mutual authentication (mTLS or signed tokens). "It's internal" is not a control |
| **User uploads** | Size and type limits, malware scanning if shared, stored outside the web root, path traversal |
| **Outbound fetches** | SSRF: block private and metadata IP ranges after DNS resolution |
| **Data stores** | Encryption at rest, least-privilege credentials per service, backups protected from the same credentials |
| **ML inputs** | Adversarial (evasion) inputs, poisoning if retraining on user data, model extraction through repeated queries |
| **Physical sensors** | Spoofing or replay of one sensor; require cross-sensor agreement before acting |
| **LLM tool use** | Instructions injected through retrieved content, over-broad tool permissions, secrets in the context window |
