---
name: scale-refactor
description: Refactor a working prototype toward production shape — surfacing scaling bottlenecks, adding observability, and hardening the trust boundaries it actually crosses — without a wholesale rewrite that loses working behavior. Use when code that started as a proof-of-concept or hackathon-speed build needs to survive real load, real failures, or a real audit, or when the user says something like "this works, now make it not fall over."
---

# Scale Refactor

A prototype and a production system aren't different in cleverness — they're different in what assumptions they can get away with. This skill finds the assumptions that were fine for a demo and won't survive contact with real load, and fixes them incrementally instead of rewriting the working parts.

## Step 1 — Find the assumptions that break first, not everything at once

Look specifically for:
- **Single-instance state** — anything held in a local variable or in-process cache that silently breaks the moment there's more than one instance running.
- **Unbounded collections/queues** — anything that grows with input volume with no cap, backpressure, or eviction policy.
- **Synchronous calls that will become the bottleneck** — a call chain that's fine at demo QPS and serializes badly at real QPS; identify which one hits the wall first, not all of them equally.
- **No backpressure** — a producer with no way to signal or respond to a slow consumer, so load just piles up until something falls over.

Rank these by which one actually breaks first under realistic load — fixing the fifth-order bottleneck before the first-order one wastes the refactor.

## Step 2 — Add observability at the points that matter

Not blanket logging everywhere — structured logs and metrics at the specific decision points and failure modes identified in Step 1, plus trace propagation across the async/service boundaries the request actually crosses. The test: when this breaks in production, will the existing observability tell you *why*, or just *that* it broke?

## Step 3 — Harden the trust boundaries this code actually crosses

While already touching this code, check the boundaries it crosses (see `secure-code-review` for the full checklist) — a scale refactor is a natural point to fix a validation gap the prototype phase skipped, since the code is already open and under test.

## Step 4 — Do it incrementally

Change what needs to change for Steps 1-3; don't rewrite working logic along the way just because it's now visible. Track a before/after list: what changed, why, and what was deliberately left alone because it wasn't the bottleneck. A refactor that can't say what it left untouched is really a rewrite wearing a refactor's name, and rewrites lose working behavior that prototypes often don't have tests to catch.

## Output

State the ranked bottleneck list from Step 1, what was actually changed and why, what observability was added and what failure it's meant to surface, and what was explicitly left alone.
