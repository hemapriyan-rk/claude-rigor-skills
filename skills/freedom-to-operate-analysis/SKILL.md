---
name: freedom-to-operate-analysis
description: Assess whether building and selling a specific product or process risks infringing an active third-party patent — a different question from whether your own invention is novel. Use before committing to productize or commercialize anything patent-adjacent, or whenever the user asks "can we actually ship this without getting sued" or "is this clear to build." This is a technical infringement-risk scoping exercise, not legal advice — a formal opinion requires a patent attorney.
---

# Freedom-to-Operate Analysis

Novelty and freedom-to-operate are independent questions, and conflating them is the single most common mistake here: an invention can be perfectly novel and patentable while the *product built around it* still infringes someone else's active, unrelated patent on a component or method the product also happens to use. This skill checks the second question, which `patent-novelty-evaluator` does not answer.

## Step 1 — Define the actual product, not the invention

FTO is about what gets built and sold, not the claimed invention in isolation. List every distinct technical element of the actual as-built product/process — including the "obvious" supporting components, not just the novel one — since any of them can independently infringe. State the jurisdiction(s) of manufacture and sale explicitly: patent rights are territorial, so clearance in one country says nothing about another.

## Step 2 — Search for active, in-force patents specifically

This differs from a novelty search in one critical way: status matters. A patent that's expired, lapsed for non-payment of fees, or been invalidated is prior art for novelty purposes but is **not** an infringement risk — it's in the public domain. Search patent databases (Google Patents, Espacenet, national patent office registers) and check the current legal status of every candidate hit, not just its existence.

## Step 3 — Claim-by-claim comparison against every product element

For each active patent found that's remotely relevant, compare **every claim** (not just the broadest independent claim) element-by-element against the actual product's implementation. Infringement is assessed claim-by-claim: a product can avoid the broadest claim and still infringe a narrower dependent claim, or vice versa. Also consider whether an element that differs literally might still be caught under the doctrine of equivalents (performs substantially the same function, in substantially the same way, to achieve substantially the same result) — a purely literal comparison understates real risk.

## Step 4 — Classify each finding

- **Blocking** — the product as designed reads directly onto an active claim, no workaround identified yet.
- **Design-around available** — infringement risk exists, but a specific, named change to the implementation avoids it (state the change precisely — "use a different X" is not specific enough).
- **Clear** — no active patent claim reads onto this element as currently implemented.

## Step 5 — Check for pending risk, not just granted patents

Published pending applications aren't enforceable yet but can still grant later, and their claims often broaden or narrow during prosecution — flag any pending application in the same space as a forward-looking risk, not just a note for later.

## Output

```
# FTO scan: [product/process], jurisdiction(s): [...]

## Active patents found, by relevance
| Patent | Status | Claim(s) implicated | Classification (Blocking / Design-around / Clear) | Notes |

## Pending applications to watch

## Overall read
[Clear / design-around plan needed / blocked — state which, and why]
```

State plainly, every time: this is a technical scoping exercise to inform a decision, not a legal opinion, and a formal freedom-to-operate opinion for any real commercialization decision needs a patent attorney with access to complete, current search tools and jurisdiction-specific expertise.
