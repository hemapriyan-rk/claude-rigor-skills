# Architecture: Live driver locations (40k drivers, ride-hailing, one region)

## Requirements

**Given:** 40,000 active drivers, one GPS fix each every 4 s, riders see nearby drivers within 1 s, 99.9% availability, one cloud region, 4 engineers.

**Assumptions** (shout if any are wrong, because they change the design):

| Item | Assumption | Derived |
|---|---|---|
| Write load | 40k ÷ 4 s | **10k writes/s**, ~64 B payload, about 4 MB/s on the wire with headers |
| Read load | 20k riders with the map open, refreshing every 2 s | **~10k reads/s** |
| Active state | 40k × ~100 B | **~4 MB**. Memory is not the constraint; ops/s and failover are. |
| "Within 1 s" | p99 time from a fix arriving to it being queryable < 1 s, and p99 query latency < 300 ms | Data age is bounded by the 4 s GPS interval, so a rider sees a position that is 4–6 s old. The client smooths this by extrapolating from heading and speed. |
| Availability | 99.9% | 43.8 min/month error budget |
| Durability | Live positions are ephemeral. History is best-effort and used for analytics only, not for fares or disputes. | If trip traces are needed for fares, that's a separate durable path with the driver app buffering. This design doesn't cover it. |
| Cloud | AWS names for concreteness, 3 AZs. Rough cost is low thousands USD/month, an estimate only. | |

## Trade-offs

- **Live location is AP, last-write-wins per driver by sequence number.** A stale or lost fix is replaced in 4 s anyway. This gives up exactness of any single fix.
- **Hot store is one in-memory Redis (primary plus replica in another AZ), no persistence, no sharding at day one.** 10k scripts/s is about 10–20% of one node. It gives up horizontal headroom beyond ~5× (see break scenario 1) and accepts a 30–90 s failover blip. The state refills from live traffic in 4 s, so there is no restore step.
- **Ingest to Redis is synchronous (about 5 ms). Ingest to history is asynchronous through a stream with a bounded buffer.** A stream outage creates gaps in history. It never affects the live map.
- **Readers poll every 2 s instead of holding WebSocket subscriptions.** This gives up push immediacy. In exchange, reads are stateless and cacheable, and there is no reconnect-storm class of failure for a 4-person team to operate.
- **Ingest is stateless HTTPS POST with keep-alive behind an ALB, not WebSocket or MQTT.** This gives up some mobile-battery efficiency. Fewer moving parts.
- **Query results are cached in-process for 500 ms per cell-ring.** Redis reads scale with the number of cells, not riders. It adds up to 0.5 s of staleness.
- **Under overload, ingest sheds writes** (returns `429` with `next_interval_ms`) instead of queueing. The next fix arrives in 4 s anyway, so a queue would only deliver stale data.
- **State ownership:** Redis owns the current position, and the driver app is the source of truth. If they disagree, the higher `seq` wins. The stream and S3 own history.
- **Rejected alternative:** drop Redis and have each query node consume the stream into in-memory state (it's only ~4 MB). It removes a stateful tier, but it puts the stream on the critical path and adds rebuild and replay logic. It is the escalation path if Redis becomes the problem.

## Diagram and boundary data

```mermaid
flowchart LR
  D[Driver app] -->|HTTPS POST /v1/location<br/>JSON {lat,lon,acc,hdg,spd,seq}<br/>JWT driver token| ALB1[ALB]
  ALB1 --> ING[Ingest service<br/>ECS x6, 3 AZ]
  ING -->|Lua: seq check, move cell<br/>~5ms| R[(Redis primary<br/>+ replica other AZ<br/>TTL 30s, no persistence)]
  ING -.->|async, bounded buffer| K[[Stream<br/>Kinesis/MSK]]
  K --> W[History worker] --> S3[(S3 / Timescale<br/>30-day history)]
  RD[Rider app] -->|HTTPS GET /v1/nearby?lat&lon<br/>JWT rider token<br/>poll 2s| ALB2[ALB + WAF]
  ALB2 --> Q[Query service<br/>ECS x4, 3 AZ<br/>500ms cell cache]
  Q -->|HGETALL x7 cells, pipelined| R
  Q -->|ephemeral ids, quantized coords| RD
```

| Boundary | Data | Format / protocol |
|---|---|---|
| Driver → Ingest | One fix: lat, lon, accuracy, heading, speed, client `seq`. Server stamps its own receive time. | JSON over HTTPS, JWT |
| Ingest → Redis | `drv:{id}` → (cell, seq); `cell:{h3r7}` → hash of id → packed(lat, lon, ts, hdg). Key TTL 30 s. | RESP over TLS, one Lua call |
| Ingest → Stream | Same fix plus server time | Protobuf, fire-and-forget |
| Query → Redis | The rider's H3 res-7 cell plus 6 neighbors (about 3 km), `HGETALL` pipelined, filtered to `ts` < 10 s old, nearest 20 returned | RESP over TLS |
| Query → Rider | ≤ 20 vehicles: ephemeral id, coarse position, heading | JSON |

## Failure modes

| Component | Down | Slow | Bad data / overloaded | Behavior |
|---|---|---|---|---|
| **Redis** | Failover 30–90 s. Writes fail, so ingest returns 503 and drivers retry on the next tick. Query serves the in-process cache for up to 10 s, then returns an empty list with `degraded:true`. | Ingest timeout 50 ms, with a circuit breaker that sheds writes. | Memory is bounded by TTL and driver count. The cell-hash key for a dense cell (an airport) can reach thousands of entries, so cap the response at 20 and keep `HGETALL` sizes monitored. | **Degrades, then self-heals** within ~4 s of Redis returning. |
| **Ingest service** | The ALB drops the unhealthy task and the other AZs carry the load (N+1 per AZ). | Per-request deadline 200 ms. Clients don't retry within the same tick, which prevents retry storms. | Malformed or out-of-range input gets a 400 and is never written. Old `seq` is a no-op. | Degrades |
| **Query service** | Same as ingest. | The cache absorbs bursts. | A rider querying a huge empty area still reads only 7 cells. | Degrades |
| **ALB / WAF** | Multi-AZ managed. A deep health check hits `/healthz` and does a Redis `PING`. | | Rate limits apply. | Fails if the whole region fails (accepted, one-region scope). |
| **Stream / worker** | Ingest buffers 5 s of points, then drops them. | Consumer lag grows. Retention (24 h) is far beyond any realistic lag. | A poison message goes to the DLQ. | **No effect on the live map** |
| **Driver app / network** | A driver offline for hours disappears from the map after 30 s TTL (correct). | | A buffered burst on reconnect: the client sends only the latest fix live, and `seq` ordering discards any stale ones. | Degrades |
| **Clock drift** | Client time is never trusted for freshness. Freshness uses server receive time, ordering uses `seq`. | | | Handled |

## Threat model

| Boundary | Attack | Control | Residual risk |
|---|---|---|---|
| Driver → Ingest | Spoof another driver's location (IDOR) | `driver_id` comes only from the JWT claim, never the body. Tokens are short-lived (1 h) and revocable. | A stolen token lets the attacker spoof until it expires or is revoked. |
| Driver → Ingest | Fake location: teleporting, NaN, or out-of-range coordinates | Range checks, speed plausibility (reject jumps > ~200 km/h), accuracy field required | **A real driver with a GPS spoofer** (gaming airport queues or surge) passes these checks. Needs fraud signals outside this system. |
| Driver → Ingest | Flood from a valid token or botnet | WAF rate limit per IP and per driver (≤ 1 req / 2 s), body ≤ 1 KB, load shedding | A volumetric DDoS needs the provider's L3/L4 protection (AWS Shield). |
| Rider → Query | **Scraping:** moving the query point to map every driver, or stalking a specific driver | Authenticated riders only, per-rider rate limit, fixed radius, ≤ 20 results, ephemeral ids that rotate, coordinates quantized to ~25 m | A determined scraper with many accounts still samples the map. Slow it down, can't stop it. |
| Rider → Query | Query with crafted `lat/lon` to force large reads | Validated range, only 7 cells read, cache | None significant |
| Service → Redis | Lateral movement reads all positions | Redis in a private subnet, TLS plus ACL users (ingest write-only on its keys, query read-only), SG limited to the two services | A compromised service can do what its role allows. |
| History store | Long-term location trails are personal data | Encrypted at rest, 30-day lifecycle, least-privilege analytics role | Retention and legal basis are policy decisions, not covered here. |

## Observability

| Signal | Detects | Pages? |
|---|---|---|
| **Canary driver** posts a fix every 4 s, and a canary rider polls for it. Metric: end-to-end visible age p99. | The headline requirement: the 1 s pipeline and any hidden outage | **Yes** (> 1 s for 3 min) |
| Availability SLI (2xx / total on both APIs), with burn-rate alerts (e.g. 14× over 5 min) | The 99.9% target | **Yes** |
| Redis CPU, ops/s, latency p99, failover events, memory | Saturation, failover | Yes for failover or CPU > 70% sustained |
| Active-driver count (distinct fixes in last 10 s) dropping > 30% in 1 min | Mass failure upstream of dashboards: a bad app release, auth outage, regional network problem | **Yes** |
| 429 / shed rate and 4xx/5xx by cause | Overload, abusive clients, bad releases | Ticket, page if sustained |
| Ingest 400s for implausible jumps, per driver | GPS spoofing or a broken app build | Ticket |
| Stream consumer lag, DLQ depth | History gaps | Ticket |
| Cert expiry, JWT key rotation age | Silent auth failure | Ticket |

## Break scenarios

| Scenario | What breaks first |
|---|---|
| **10× load** (100k writes/s, 100k reads/s) | **Redis CPU** saturates (a single node tops out around 100–200k simple ops/s, less with Lua). Reads are fine because the cell cache collapses them. Behavior: breaker trips, ingest sheds writes, and the map gets staler instead of failing. Fix path: shard Redis by region using a `{region}` hash tag so a driver's keys co-locate. Shard by region from the start in the key naming, even though it's one node today. |
| **Redis unavailable 15 min** (failover failed) | The map goes empty after the 10 s cache window, and the SLO burns 15 of the 43.8 min monthly budget. **Undefined: does dispatch matching read this store?** If it does, rides stop being matched during the outage. Decide this before launch. Mitigation: IaC can rebuild a cluster in ~10 min with no data restore, since traffic refills it in 4 s. For a stronger guarantee, add a second small Redis that ingest dual-writes to. |
| **Malicious or malformed input** on ingest | Bad JSON and out-of-range values are rejected at validation. A valid-token flood hits the rate limit and then shedding. A stolen token spoofing a driver is the real exposure (see threat model). Nothing crashes. |

## Weakest point

1. **Redis is the single stateful component, and its failover (30–90 s) plus the unresolved dispatch coupling is the biggest risk to 99.9%.** One bad failover plus one bad release in a month can exhaust the 43.8 min budget. Settle two things first: whether dispatch depends on this store, and whether you want the dual-write standby.
2. **"Within 1 second" is only achievable for pipeline latency.** Rider-visible position age is 4–6 s because of the GPS interval. If the product requirement means the *map* must be ≤ 1 s fresh, the driver cadence has to change (a 1 s interval is 40k writes/s and needs sharding on day one).

If you want, I can write this up as a doc or turn it into a handoff brief for implementation.