---
name: mobile-platform-architecture
description: Design mobile-specific architecture — offline-first sync strategy, background execution limits, native/cross-platform bridge boundaries, battery- and network-aware behavior, and process-death state restoration — for iOS, Android, or cross-platform frameworks. Use when architecting a mobile app or reviewing one for reliability/battery problems. Distinct from `frontend-architecture`, which covers web rendering strategy and browser-side state — this is mobile OS-specific constraints.
---

# Mobile Platform Architecture

Code that works perfectly in a mobile simulator with a stable connection and an app that never gets backgrounded tells you almost nothing about how it behaves in the field. This skill designs against the actual constraints mobile OSes impose, not the friendlier development environment.

## Step 1 — Decide offline-first vs. online-only, explicitly

If offline support is needed, define the sync strategy up front: last-write-wins, a CRDT-based merge, or manual conflict resolution surfaced to the user — and state explicitly what happens when a local-only change collides with a remote change made elsewhere. "We'll figure out conflicts later" is how sync bugs become the app's most reported issue.

## Step 2 — Design against real background-execution limits

Both major mobile platforms impose hard limits and kill policies on background work — a naive background thread or timer will not simply keep running. State exactly what genuinely needs to run in the background (sync, notifications, location updates) and design it against the platform's actual scheduled/deferred-execution mechanisms, not an assumption that background work behaves like a server process.

## Step 3 — Define bridge/platform-channel boundaries deliberately (cross-platform frameworks)

For any cross-platform framework, decide explicitly what crosses the native/framework bridge and account for the serialization cost of doing so on each crossing. Distinguish what genuinely needs a native module (platform APIs the cross-platform layer doesn't expose well) from what the framework already handles adequately — reaching for native modules by default adds maintenance surface for no benefit.

## Step 4 — Make battery and network condition explicit design inputs

Prefer push over polling wherever available — polling on a schedule costs battery even when nothing changed. Design behavior for degraded/intermittent connectivity explicitly (retry/backoff, offline queuing) rather than assuming a persistent low-latency connection, which is the exception in real mobile use, not the rule.

## Step 5 — Design for process death and state restoration

Mobile OSes kill backgrounded apps to reclaim resources. State explicitly what must survive that (in-progress user input, navigation state, an unsent action) and how it's persisted, versus what can be safely lost and cheaply re-fetched on next launch. An app with no stated answer here loses user work unpredictably and calls it "a rare bug."

## Step 6 — Request permissions minimally and contextually

Request the minimum permission set actually needed, at the point of use rather than all at app launch, and design an explicit fallback behavior for when a permission is denied — a feature that assumes a permission was granted and crashes or silently no-ops when it wasn't is a design gap, not user error.

## Output

```
# Mobile architecture: [app]
## Offline strategy and conflict resolution
## Background execution: what runs, and via which platform mechanism
## Bridge/native-module boundaries (cross-platform only)
## Battery/network-aware behavior
## Process-death state restoration: what's preserved, how
## Permission requests: what, when, and the denied-fallback behavior
```
