---
name: memory-leak-hunter
description: Find and fix memory leaks with proof. Shows memory grows over repeated work, finds what is holding the objects with heap snapshots or allocation diffs, fixes the reference, and re-runs the same growth test to show memory now stays flat. Python, Node.js, Java, Go.
---

# Memory Leak Hunter

"Memory keeps going up" has three different causes: a real leak, a cache that is still warming up, and allocator fragmentation. Fixing the wrong one wastes days. Prove the growth, find the object chain that keeps memory alive, cut it, and show the same test now stays flat.

## 1. Set scope and budget

- **Start from the reported symptom:** which process, what workload, how fast it grows (for example, 80 MB to 2 GB in a day).
- **Read the references with the code.** In the same step as the suspect code, read `references/tools.md` and `references/leak-patterns.md` from this skill's base directory.
- **Work on a reproduction, not production.** Build a small harness that repeats one unit of work (a request, a job, a message) many times.

## 2. Prove the growth

- Run the unit of work N times, force a garbage collection, and record memory at checkpoints: for example after 1k, 2k, 4k and 8k iterations. Use the runtime's own heap measure (see the tools table), not only process RSS.
- Classify the curve:
  - **Grows in proportion to iterations:** a leak. Continue.
  - **Rises, then flattens:** a cache or pool warming up. Check its size limit, then stop.
  - **RSS grows but the heap doesn't:** fragmentation or native memory. Say so; the fix is different.
- Record the growth per iteration (for example, 1.9 KB per request). That number is what the fix must remove.

## 3. Find what holds the memory

- Take two heap snapshots or allocation snapshots, at checkpoint k and 2k, and diff them. The types and allocation sites that grew by about the iteration count are the leak.
- Follow the reference chain from those objects back to a root: a global, a module-level dict, a class attribute, a registered listener or callback, a closure, a thread or goroutine that never ends.
- Match the chain against `references/leak-patterns.md`. State the retainer in one line, naming the root, the container and the objects it keeps alive.

## 4. Fix the reference, not the symptom

- Remove what holds the object: unsubscribe the listener, bound and evict the cache, close the resource, cancel the context, let the thread end, use a weak reference where ownership is genuinely optional.
- Don't "fix" a leak by raising memory limits, restarting the process on a schedule, or calling the garbage collector more often. Mention those only as stopgaps.
- Keep the change as small as the cause.

## 5. Verify with the same test

- Re-run the exact harness from step 2 with the same iteration counts.
- Show memory now flattens, and give before and after growth per iteration.
- Run the project's tests, or a quick behaviour check, to confirm the fix didn't change what the code does. A removed listener that was still needed is a bug, not a fix.

## Output

```
## Result
Growth: <before> per <unit> → <after> per <unit>, over <N> iterations. Behaviour unchanged: <how checked>.

## Cause
<the retaining reference chain, one line>, with the snapshot evidence (type, count, size growth).

## Change
<the fix>, and why it removes the reference rather than hiding it.

## Remaining risk
<anything not covered: native memory, other workloads, caches that are bounded but large>.
```

For example: *"Growth: 3.1 KB per job → 0.0 KB per job over 10,000 jobs. `@lru_cache(maxsize=None)` on `render(template, context_id)` kept every context because each `context_id` is unique; the `tracemalloc` diff showed 10,000 new cache entries."*
