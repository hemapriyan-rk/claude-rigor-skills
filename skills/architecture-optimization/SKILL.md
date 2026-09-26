---
name: architecture-optimization
description: Optimize an existing, already-working system architecture or deployment for cost, latency, or resource efficiency — right-sizing compute, caching strategy, autoscaling policy, service-boundary reconsideration. Use when cost or latency needs to come down on a system that already works, without a ground-up redesign. Distinct from designing a new system (use `architecture-design` for that) and from code-level refactoring (use `scale-refactor` for that) — this operates on infrastructure and deployment decisions.
---

# Architecture Optimization

Optimizing the component that's easiest to change instead of the one that's actually expensive or slow is the default failure mode here. This skill forces measurement before any lever gets pulled.

## Step 1 — Measure before optimizing anything

Get the actual cost breakdown (spend per component, not a total) and the actual latency breakdown (where end-to-end time is really spent, via tracing — not assumption). Optimizing without this is optimizing a guess.

## Step 2 — Check the high-leverage levers, in this order

1. **Caching** — what's cacheable and isn't cached yet; for what's already cached, is invalidation actually correct, or is stale data being served past its real validity window?
2. **Right-sizing compute** — always-on provisioning for bursty load (paying for peak 24/7) versus autoscaling or serverless fit for the actual traffic shape.
3. **Data locality** — cross-region or cross-AZ calls that could be colocated, adding pure network latency with no other benefit.
4. **Batch vs. real-time** — anything computed per-request that could be precomputed or batched without hurting the actual user-facing requirement.

## Step 3 — Autoscaling policy correctness

Check that the scaling trigger metric actually correlates with real load — CPU-based autoscaling on an I/O-bound service is a common miss that either over- or under-scales. Check scale-down doesn't thrash (scale down, immediate re-scale up, repeat).

## Step 4 — Reconsider service boundaries if the evidence points there

Sometimes the real optimization is that a service boundary adds network overhead without buying real isolation or independent-scaling benefit. State this explicitly if the measurements support it — it's an uncomfortable finding to raise, not a reason to avoid raising it.

## Step 5 — Verify every change against the Step 1 measurement

Re-run the same cost/latency breakdown after each change and confirm it actually moved, on the metric that mattered — not a proxy metric that's easier to improve.

## Output

State the ranked cost/latency breakdown from Step 1, which lever was pulled and why it was picked over the others, and the before/after measurement for each change.
