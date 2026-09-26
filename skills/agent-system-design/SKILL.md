---
name: agent-system-design
description: Design an AI agent system's orchestration, memory/state architecture, tool-use boundaries, and cost/runaway-loop guards — the upstream design layer, before any code exists to audit. Use when designing a new single-agent or multi-agent system, or when an existing agent system is unpredictable, expensive, or hard to debug. Distinct from `ml-security-audit`, which audits code for prompt-injection risk after the fact — this designs the boundaries so that risk is scoped in from the start.
---

# Agent System Design

An agent system without explicit boundaries doesn't fail loudly — it fails by quietly running longer, costing more, or taking an action nobody would have approved if asked directly. This skill puts the boundaries in before that happens, not after an incident.

## Step 1 — Justify the architecture, don't default to it

Decide single-agent-with-tools versus multi-agent orchestration based on an actual reason: genuine parallelism need, real specialization (different agents needing different tool access or context), or isolation (one agent's failure shouldn't corrupt another's state). Multi-agent orchestration adds real coordination complexity and failure modes — "it seemed like the more sophisticated choice" is not a justification, and a single well-scoped agent is often the right answer.

## Step 2 — Design memory/state explicitly

State plainly: what's short-term (lives only in the current context window and disappears), what's long-term (persisted across sessions), what's shared across agents versus private to one, and — for shared state — what happens when two agents read stale or conflicting state. An agent system with no stated answer to "what does this agent remember and for how long" will produce behavior nobody can reason about after the fact.

## Step 3 — Scope tool access to least privilege, explicitly

Every tool an agent can call should be an explicit allow-list decision, not blanket access to everything available. This is also the seam where the highest-consequence security risk actually enters: validate tool outputs before they re-enter the agent's context, since unvalidated tool output (a fetched page, a file's contents, another agent's output) is exactly how an attacker-controlled instruction gets read as a command instead of data. Run `ml-security-audit`'s prompt-injection check against this specific boundary once code exists.

## Step 4 — Put runaway and cost guards in from the start, not as a patch later

- A maximum iteration/step count, not "the agent decides when it's done" as the only stopping condition.
- A maximum cost/token budget per task, enforced, not just estimated.
- A timeout on every individual tool call — a single hanging tool call shouldn't be able to stall the whole task indefinitely.
- Explicit termination conditions stated up front, not inferred from behavior after the fact.

## Step 5 — Design the failure and escalation path

State what happens when an agent gets stuck in a loop, when a tool call fails repeatedly, or when the agent's own confidence in a result is low: is there a defined escalation to a human, a safe-fallback action, or does the design currently just retry silently forever? An agent system with no answer here will find out the answer in production, at the worst possible time.

## Step 6 — Design for reconstructable reasoning

Tie into `observability-design`: can the agent's actual decision path be reconstructed after the fact (what it saw, what it decided, why), or only the final output? Without this, debugging an unexpected agent action is guesswork.

## Output

```
# Agent system design: [system]
## Orchestration choice and justification
## Memory/state architecture (short-term / long-term / shared / private)
## Tool allow-list and output-validation points
## Runaway/cost guards (iteration cap, budget, timeouts, termination conditions)
## Failure/escalation path
## Reasoning observability approach
```
