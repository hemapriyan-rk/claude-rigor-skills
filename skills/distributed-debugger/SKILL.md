---
name: distributed-debugger
description: Root-cause debugging methodology for concurrency, async, and distributed bugs — race conditions, deadlocks, retry storms, partial failures, message reordering, clock skew. Use when a bug is intermittent, hard to reproduce, only shows up under load, or spans multiple services/processes. Do not use for straightforward deterministic bugs — this is specifically for the class that "goes away when you add a print statement."
---

# Distributed Debugger

The failure mode this skill prevents: patching the symptom that happened to be visible in the one stack trace you got, without ever confirming the actual race or ordering bug it came from — so it comes back next week in a slightly different shape.

## Step 1 — Reproduce before touching anything

Don't fix from a hunch off a single stack trace. Get a reliable (even if not 100%) reproduction first — add logging or a stress harness if needed to make an intermittent bug show up on demand often enough to iterate against. A fix you can't verify is a guess, not a fix.

## Step 2 — Isolate the smallest failing case

Strip away everything not needed to trigger it — fewer services, fewer threads, fewer requests. The smaller the reproduction, the more likely the real mechanism is visible instead of buried in incidental noise.

## Step 3 — Check the concurrency-specific suspects explicitly

Don't just read the code sequentially — actively check for:
- **Shared mutable state accessed without a lock**, or a lock held across an operation it shouldn't be (blocking an unrelated path).
- **Check-then-act races** — a condition checked and then acted on later, with no guarantee nothing changed in between.
- **Non-idempotent retries** — a retried operation that has a side effect the first attempt already had, producing duplicates or double-counting on retry.
- **Ordering assumptions across async boundaries** — code that assumes message/event order is preserved when the transport doesn't guarantee it.
- **Timeout/backoff misconfiguration causing cascading failure** — a timeout too short for real load, triggering retries that amplify the load that caused the timeout in the first place (retry storm).
- **Clock skew / time-based logic across nodes** — anything comparing timestamps from different machines without accounting for skew.

## Step 4 — Verify the fix actually closes the window, not just narrows it

A fix that makes the bug "much rarer" without addressing the underlying race has not fixed it — it's made the next occurrence harder to reproduce and debug. Re-run the Step 1 reproduction against the fix, ideally with the stress harness cranked harder than what originally triggered it, before calling it closed.

## Output format

State plainly: the root cause (the actual mechanism, not the symptom), the smallest reproduction found, the fix, and how the fix was verified (what was re-run and what it showed). If the root cause genuinely couldn't be pinned down, say that directly instead of presenting a symptom patch as a root-cause fix.
