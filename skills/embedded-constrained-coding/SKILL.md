---
name: embedded-constrained-coding
description: Write or review code for resource-constrained targets — microcontrollers, on-device mobile/edge inference, or any environment with a hard memory/power/latency budget. Use whenever the target is not a general-purpose server, or the user mentions RAM/flash limits, battery/power budget, quantization, or cross-compilation for an embedded or mobile target. Do not use this for ordinary server/cloud code with no hard resource ceiling.
---

# Embedded / Constrained Coding

Server-side code that "should be fine, it's not doing much" is usually fine. The same instinct on a microcontroller or a phone's inference budget is how a demo that worked on a dev board dies in the field. This skill forces the budget to be explicit before code gets written, and checks it was actually respected after.

## Step 1 — State the actual budget before writing anything

RAM, flash/storage, power draw, and latency ceiling — as numbers, not "should be small." If the user hasn't stated them, ask or use the documented figures for the stated target (the specific chip's actual SRAM/flash ceiling, the specific device's actual thermal/battery constraints for sustained inference) rather than assuming server-class headroom.

## Step 2 — Avoid patterns that are fine on a server and dangerous here

- **Dynamic allocation that fragments a constrained heap** — repeated alloc/free of varying sizes on a device with no memory compaction will eventually fail even when total free memory looks sufficient. Prefer static allocation or fixed pools where the target supports it.
- **Assuming the standard library behaves the same** — many embedded toolchains ship cut-down or different-behaving libc equivalents; verify rather than assume.
- **Blocking calls inside interrupt handlers or tight real-time loops** — a call that's harmless latency on a server can blow a hard deadline or starve the watchdog here.
- **Ignoring watchdog timers** — any loop or blocking operation that can run long enough to trip the watchdog needs an explicit reset/yield point.

## Step 3 — Quantization and precision tradeoffs must be measured, not assumed

If the code quantizes a model or reduces precision to fit the budget, the accuracy/latency tradeoff needs an actual measurement on representative input — "should still be accurate enough" is not a result. State what was measured and on what data.

## Step 4 — Verify against the stated budget, don't just estimate

After writing the code, check it against the Step 1 numbers concretely (actual memory profiling on-target or via the toolchain's reporting, actual measured latency/power on the target device or a faithful simulator) — "this should fit" is exactly the assumption that doesn't survive a prototype-to-field transition. If it can't be measured in this environment, say so explicitly rather than presenting an estimate as a verified fit.

## Output

State the budget assumed, what was done to fit it, and what was actually measured versus estimated. Flag anything that's an estimate rather than a measurement so it doesn't get treated as verified later.
