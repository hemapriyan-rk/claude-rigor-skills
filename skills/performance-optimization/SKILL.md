---
name: performance-optimization
description: Make slow code or systems faster by measuring first. Profile the real hot path, fix algorithmic complexity before micro-optimizing, and verify with the same measurement. Use when something is slow or needs to be faster. Never guesses at the bottleneck.
---

# Performance Optimization

"It's probably the loop" without a profile is a guess that costs a day when it's wrong. Measure, fix the biggest thing the measurement shows, measure again, and stop when the target is met.

## 1. Set scope and budget

- **Agree on the target.** What metric (p50/p95 latency, throughput, runtime, memory), on what input, and what number counts as done. If the user didn't give one, propose one and continue.
- **Stop when the target is met.** Don't keep optimizing past it. Each extra change adds risk for no requested benefit.
- **Load the tool list.** Read `references/profilers.md` from this skill's base directory together with the code, in the same step. It names the right profiler and benchmark method for the language at hand.

## 2. Measure before changing anything

- Reproduce the slowness with a repeatable command and record the baseline number. Use realistic input size: a 100-row test hides an O(n²) that 1M rows exposes.
- Profile the dimension that matches the complaint: CPU, wall-clock/I-O wait, memory, or database queries.
- If you can't run code in this environment, say so, give the user the exact profiling command to run, and work from their output. Don't present a guess as a measurement.

## 3. Classify the bottleneck

From the profile, decide which kind it is:

- **CPU-bound:** time is spent computing.
- **I/O-bound:** time is spent waiting on network, disk, or database. A faster loop changes nothing here.
- **Memory-bound:** allocation, garbage collection, or swapping dominates.

Pick the fix direction only after this.

## 4. Fix in order of leverage

1. **Algorithm or query shape:** O(n²) → O(n log n), N+1 queries → one batched query, repeated work → computed once. This usually beats everything else combined.
2. **Data structure:** list membership → set lookup, repeated string concatenation → join or a buffer.
3. **I/O pattern:** batching, concurrency, caching, an index.
4. **Micro-optimization:** only if the profile still points at the same spot after 1–3.

Don't touch code that isn't on the hot path, however inefficient it looks.

## 5. Verify the same way

Re-run the exact baseline command on the same input. Report before and after on the metric that was agreed, and confirm the output is unchanged (same result, or the test suite passes). A faster wrong answer is a regression.

## Output

```
## Result
<metric>: <before> → <after> (<n>× faster) on <input>.

## Bottleneck
<what the profile showed, with the key numbers>, <CPU / I-O / memory>-bound.

## Change
<the fix, as a diff or code>, and why it was picked over the alternatives.

## Verified
<command re-run>, <output unchanged: how checked>.
```

For example: *"Runtime: 41.8 s → 0.6 s (70×) on 50,000 rows. `cProfile` shows 97% of time in `list.__contains__` inside `dedupe()`: membership tests on a list, O(n²)."*
