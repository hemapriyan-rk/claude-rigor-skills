---
name: architecture-design
description: Design or review a system architecture with explicit trade-offs, failure modes, a threat model, and break scenarios. Use for "how should I architect X" questions involving scale, distributed state, edge/cloud, ML, or agents. Not for scaffolding a single simple service.
---

# Architecture Design

A diagram of boxes and arrows is not an architecture. An architecture is a set of trade-offs someone decided on purpose, plus an account of how the system fails. This skill produces both.

## 1. Set scope and budget

- **Match depth to the stakes.** A prototype or internal tool gets the **short form**: requirements, the three most important trade-offs, the top five failure modes, and the weakest point. A production system, anything handling money or personal data, or anything with ML or edge components gets the **full form** below.
- **Get the numbers, once.** If load, latency, availability, or cost targets are missing, ask for them in a single message of at most three questions. If the user can't or won't answer, state your assumptions as numbers and continue. Don't stall.
- **Reviewing an existing design?** Read the design doc or code you were given before proposing anything. Don't redesign parts that already work; say what you'd keep.
- **Load the checklist with the requirements.** Before step 4, read `references/failure-modes.md` from this skill's base directory. It lists failure modes and threats by component type, so you check against it instead of recalling them from scratch.

## 2. Requirements

- **Functional:** what the system must do, in a few bullets.
- **Non-functional, as numbers:** throughput, latency target (with percentile), availability, data durability, consistency needs, cost ceiling, and power or bandwidth budget for edge parts. "Fast" and "scalable" aren't requirements.

## 3. Decide the trade-offs

Name each decision and what it gives up. At minimum:

- Consistency vs. availability when the network partitions, and where in the system that line sits.
- Synchronous vs. asynchronous calls between components, and what happens when a downstream service is slow.
- Edge vs. cloud placement, and what happens when the connection between them drops.
- Who owns each piece of state, and which copy wins when two disagree.

Write each as one line, for example: *"Ride requests are written to Postgres synchronously (consistency) and fanned out to drivers through a queue (availability). A queue outage delays dispatch; it doesn't lose rides."*

If a design can't say which side it picked, the decision was deferred to production.

## 4. Components, data flow, and failure modes

- Draw the components and data flow as a Mermaid diagram, and list what crosses each boundary (data, format, protocol).
- For each component, use the checklist to state what happens when it is **down, slow, overloaded, or fed bad data**, and whether the system degrades or fails. For any ML component, state the fallback for low-confidence or out-of-distribution input.

## 5. Threat model

For each trust boundary in the diagram: what can an attacker send across it, what control stops them, and what stays exposed after that control. Include the ML and sensor threats from the checklist if those components exist.

## 6. Observability

Name the few signals that would detect each top failure mode from step 4, and which ones page someone. A failure you can't detect will be found by users.

## 7. Break it before calling it done

Walk through three concrete scenarios and say what breaks first in each:

1. 10× the expected peak load.
2. The most important stateful component unavailable for 15 minutes.
3. A malicious or malformed input on the most exposed path.

If any answer is "undefined," that is the design's weak point. Say so.

## Output

```
# Architecture: <system>
## Requirements (numbers, with stated assumptions)
## Trade-offs (one line each: decision → what it gives up)
## Diagram (mermaid) and boundary data
## Failure modes (component → down / slow / bad data → behavior)
## Threat model (boundary → attack → control → residual risk)
## Observability (signal → failure it detects → pages?)
## Break scenarios (scenario → what breaks first)
## Weakest point
```

Keep it as short as the stakes allow. A table row beats a paragraph.
