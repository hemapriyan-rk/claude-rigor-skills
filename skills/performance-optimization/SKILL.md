---
name: performance-optimization
description: Profiling-driven performance optimization — measure the actual hot path before changing anything, fix algorithmic complexity before micro-optimizing, verify improvement with the same measurement that found the problem. Use whenever code or a system needs to be faster, or the user says something is slow. Do not use this to justify guessing at what's slow — that's the exact failure mode it exists to prevent.
---

# Performance Optimization

"It's probably the loop" without a profile is a guess that costs a day when it's wrong. This skill makes measurement the first step, not an afterthought used to justify a fix already decided on instinct.

## Step 1 — Measure first, always

Get an actual profile (CPU, memory, I/O wait — whichever dimension matches the complaint) before changing a single line. If profiling tooling isn't set up yet, setting it up is step 1, not a skippable nicety.

## Step 2 — Identify the bottleneck class before picking a fix

CPU-bound, I/O-bound, and memory-bound problems need completely different fixes. A CPU micro-optimization on an I/O-bound path (waiting on a network call or disk) does nothing — confirm which class this actually is from the Step 1 profile before choosing a direction.

## Step 3 — Fix in this order of leverage

1. **Algorithmic complexity** — an O(n²) → O(n log n) change beats any constant-factor optimization at real scale; always check this first.
2. **Data structure choice** — the right structure for the actual access pattern (see `database-design` for the same principle applied to schemas) often removes the need for the next step entirely.
3. **Micro-optimization** — inlining, avoiding allocations in a hot loop, reducing redundant work. Only worth doing once the profile shows this specific spot is still the bottleneck after the first two.

## Step 4 — Don't over-correct into premature optimization

The profile decides what's worth touching — not intuition about what "looks inefficient." A path that isn't on the critical path per the Step 1 measurement doesn't need optimizing regardless of how it reads; touching it burns time and adds risk for no measured benefit.

## Step 5 — Verify with the same measurement, on the metric that actually matters

Re-run the exact profile or benchmark that identified the problem — not a different, easier-to-pass one — and confirm the user-facing metric (actual latency, actual throughput) improved, not just a proxy that's easier to move.

## Output

State the bottleneck identified (with the profile evidence, not just an assertion), the fix applied and why it was picked over other options at that leverage level, and the before/after measurement from the same profiling method.
