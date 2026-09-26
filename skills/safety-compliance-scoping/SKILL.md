---
name: safety-compliance-scoping
description: Scope which safety and regulatory compliance frameworks plausibly apply to a system — functional safety standards, medical device classification pathways, industrial safety directives — based on its actual use case and failure consequence, before deep technical or product investment. Use early, whenever a system's use case touches health, safety, or regulated industrial contexts, to identify what compliance burden is coming rather than discovering it after the architecture is locked in. This produces a scoping map, not a certification — a qualified regulatory/compliance professional and, where relevant, legal counsel must own the actual compliance path.
---

# Safety Compliance Scoping

The expensive mistake here isn't picking the wrong standard — it's making architecture decisions before anyone checked which standards apply, then discovering the required risk classification or traceability regime demands changes that are painful to retrofit. This skill exists to surface that early, cheaply, before the fact.

## Step 1 — Classify the actual use case and consequence of failure first

Everything downstream depends on getting this right: is the system providing decision support to a human who remains in control, or acting autonomously with a direct real-world effect? Is the context consumer, industrial, or medical? What's the realistic worst-case consequence if it fails or gives a wrong answer? This classification — not the technology used to build the system — determines which regulatory framework applies at all.

## Step 2 — Identify candidate frameworks by domain, not exhaustively

Name the frameworks plausibly relevant to the Step 1 classification, for example:
- **Functional safety**: IEC 61508 as the base standard, with domain-specific derivatives (ISO 26262 for automotive, IEC 62304 for medical device software, IEC 61511 for process industry) where applicable.
- **Medical device regulatory**: a jurisdiction's device classification pathway (e.g., FDA risk-based device class in the US, EU MDR risk class in Europe) — classification usually depends on intended use and risk, not just the underlying technology.
- **Industrial safety**: relevant machinery or workplace-safety directives for the jurisdiction and industry in question.
Name only what's plausibly relevant to the actual use case from Step 1 — a system with no medical or autonomous-actuation component doesn't need the full medical-device framework listed just for completeness.

## Step 3 — State each framework's high-level requirement burden

For each candidate framework, summarize at a scoping level what it actually demands: documented risk assessment, requirement-to-test traceability, a specific validation/testing regime, independent audit or certification body involvement. This is enough to scope effort and timeline — not enough to execute compliance from.

## Step 4 — Flag the earliest expensive-to-retrofit decision points

Identify where in the system's design certain architecture or documentation decisions become expensive to redo once made — a risk classification arrived at late often invalidates architecture choices made before it, and a system built without traceability from requirements to tests from the start is far more expensive to retrofit than to build in from day one. This early flag is the actual value of scoping before deep investment, not after.

## Step 5 — State the limits of this exercise plainly

This produces a scoping map — a reasoned starting point for the actual compliance path, not a certification and not a substitute for one. The real path requires a qualified regulatory/compliance professional, and for anything safety-critical or medical, legal counsel, engaged before any compliance claim is made or any certification process is started.

## Output

```
# Compliance scoping: [system]
## Use-case classification and failure consequence
## Candidate frameworks and why each might apply
## High-level requirement burden per framework
## Earliest architecture/documentation decisions this affects
## Explicit limits of this scoping (not a certification)
```
