---
name: architecture-design
description: Design or review system architecture for distributed systems, AI/ML infrastructure, edge-cloud pipelines, or AI agent systems — with mandatory trade-off decisions, failure-mode analysis, and a security/adversarial pass, not just a component diagram. Use whenever the user is designing a new system, refactoring an existing one, or asks "how should I architect X" for anything involving scaling, observability, distributed state, or ML components. Do not use for simple single-service app scaffolding with no distributed or ML complexity — that doesn't need this level of rigor.
---

# Architecture Design

A diagram of boxes and arrows is not an architecture. An architecture is a set of trade-off decisions that someone was forced to make explicitly, plus a description of how the system fails. This skill forces both.

## Step 1 — Requirements framing (get this explicit before designing anything)

- **Functional**: what the system actually has to do.
- **Non-functional, with numbers where possible**: latency budget, throughput, consistency requirement, availability target, cost ceiling, and — for edge/embedded components — power and thermal budget. Vague non-functional requirements ("fast," "scalable") are not requirements; push for numbers or explicit ranges.

## Step 2 — Force the trade-off decisions, don't hide them

Every non-trivial system has to pick a side on things that can't be maximized simultaneously. Make each decision explicit and state what's being given up:
- Consistency vs. availability under partition, and where in the system this boundary actually sits.
- Synchronous vs. asynchronous boundaries between components, and what breaks if a downstream service is slow.
- Where compute is placed — edge vs. cloud — and what happens when connectivity to the other side is lost.
- Who owns which piece of state, and what the source of truth is when two components disagree.

If the design avoids naming any of these, that's a sign the trade-offs weren't actually decided — just deferred to production.

## Step 3 — Component decomposition and data flow

Produce a diagram (Mermaid, in a `mermaid` code fence) showing components and data flow, plus a written description of what data crosses each boundary and in what format/protocol.

## Step 4 — Failure-mode analysis (mandatory, not optional)

Enumerate the top failure modes and what actually happens for each — not just the happy path:
- What happens when each individual component is unavailable?
- What happens under load beyond the stated capacity?
- What happens with corrupted, delayed, or out-of-order data?
- For any ML/inference component: what happens on a low-confidence or out-of-distribution input — does the system have a defined fallback, or does it silently do the wrong thing?

## Step 5 — Security and adversarial pass

Every design gets an explicit threat-model pass, not a bolted-on "add auth" line:
- Attack surface: every external input, every trust boundary.
- For ML components specifically: adversarial input risk (evasion), poisoning risk if the system retrains on live data, model/IP extraction risk if the model is exposed as a service, and — for physical sensing systems — sensor spoofing risk (relevant for any sensor-fusion or cyber-physical system).
- What's actually protected by each control, and what's still exposed after it.

## Step 6 — Observability

What's measured, what triggers an alert, and how a failure in Step 4 is actually detected in practice — not just logged and ignored.

## Step 7 — Stress-test the design before calling it done

Generate at least three concrete break scenarios and state what happens in each — not a hand-wave, actual scenarios: 10x the expected load, one core component down, a malicious/adversarial input on the ML path. If the answer to any of these is "undefined," that's the actual weak point in the design and should be named as such, not smoothed over.

## Output structure

```
# Architecture: [system name]

## Requirements (functional / non-functional with numbers)
## Trade-off decisions made (and what each gives up)
## Component diagram + data flow (mermaid)
## Failure modes and behavior under each
## Threat model / security pass
## Observability
## Stress-test scenarios and what breaks first
```

Call out the weakest part of the design explicitly at the end — every architecture has one, and naming it beats letting it surface in production.
