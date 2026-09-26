---
name: observability-design
description: Design a system's observability from first principles — SLI/SLO and error-budget definition, trace architecture across service boundaries, structured logging strategy, and alerting that stays actionable instead of degrading into noise. Use when designing new observability for a system, when an existing system is "hard to debug in production," or when alert fatigue is a stated problem. Distinct from adding a few log lines to existing code — this is the design of the observability layer itself.
---

# Observability Design

Observability that can't answer "why did this break" during an actual incident isn't observability, it's a pile of dashboards. This skill designs it so the answer is actually there when it's needed, and designs the alerting so people still trust it after month three.

## Step 1 — Define SLIs tied to actual user-facing behavior

A Service Level Indicator should measure what a user actually experiences (request success rate, latency at the percentile that matters, correctness of the result) — not an internal proxy like CPU usage that can be fine while the user-facing behavior is broken. Set the Service Level Objective as an explicit target against each SLI, and derive an error budget from it (how much failure is tolerable before it's a problem worth stopping other work for).

## Step 2 — Give each observability pillar its actual job

- **Metrics** — for counting and aggregating (rates, durations, error counts) cheaply at high volume.
- **Logs** — for the specific detail of a specific event, when you already know roughly where to look.
- **Traces** — for following one request's actual path across service/async boundaries to see where time and errors accumulate.
Using logs to do what metrics should (counting events by grepping/aggregating log lines) is expensive and slow exactly when speed matters most during an incident — assign the right pillar up front.

## Step 3 — Design trace propagation across every real boundary

Context must survive not just synchronous HTTP calls but every async boundary the request actually crosses — message queues, background jobs, batched processing. A trace that silently drops at the first queue hop isn't tracing the actual system, it's tracing the easy half of it.

## Step 4 — Alert on symptoms, not causes, and make every alert actionable

Alert on SLO burn rate (the user-facing thing that matters) rather than every underlying cause independently — a dozen different causes can all threaten the same SLO, and alerting on each separately is how alert fatigue starts. For every alert that pages someone: if there's no runbook or concrete action attached, that's a sign it shouldn't page at all — route it to a dashboard or a lower-urgency channel instead.

## Step 5 — Control cardinality deliberately

High-cardinality labels (user IDs, full URLs, unbounded free-text fields) on metrics blow up storage cost and query latency, often invisibly until the bill or the dashboard timeout arrives. Decide label cardinality as a design choice, not an accident of "just tag everything that might be useful."

## Step 6 — Design dashboards for the actual incident workflow

Top-down: user impact first, then the service most likely responsible, then the component-level detail — not a flat wall of every graph available with no path through it. A dashboard designed for "what do I check first during an incident" is a different artifact from "everything we happen to measure."

## Output

```
# Observability design: [system]
## SLIs / SLOs / error budgets
## Pillar assignment (what's a metric, what's a log, what's a trace, and why)
## Trace propagation boundaries covered
## Alerting policy: [metric, threshold, burn-rate window, runbook/action]
## Cardinality decisions
## Dashboard structure (top-down incident path)
```
