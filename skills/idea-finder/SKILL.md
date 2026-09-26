---
name: idea-finder
description: Generate genuinely novel technical/product/research ideas within a domain by finding unsolved constraint intersections — not generic brainstorming. Use whenever the user wants new invention/patent/paper/product ideas in a technical space, asks "what's a gap nobody's filled here," or wants direction before committing to a project. Every idea produced must survive a "why hasn't this been done" gut-check before being presented. Do not use for open-ended creative brainstorming unrelated to technical/patent/research output — this is for ideas that need to hold up, not for volume.
---

# Idea Finder

Most idea generation produces plausible-sounding combinations of buzzwords ("AI-powered X for Y"). That's not a gap, it's a mad-lib. This skill finds ideas at the intersection of constraints that are individually well-understood but jointly unsolved — the kind of gap that survives someone asking "wait, doesn't X already do this?"

## Step 1 — Define the search space precisely

Before generating anything, pin down:
- The domain and its actual boundaries (not "AI" — "on-device inference for battery-constrained sensor nodes").
- The target artifact: is this idea meant to become a patent, a paper, a product feature, or a project? The bar and the shape of a good idea differ for each — a patentable idea needs a novel mechanism, a paper needs a testable question, a product feature needs a user who's actually blocked today.
- Any constraints already fixed by the user's situation (hardware, budget, deadline, existing project it has to plug into).

## Step 2 — Map what's known, briefly

List the 3-5 dominant existing approaches in this space and, for each, the specific limitation it has — not "it's not good enough" but the actual mechanism of failure (latency bound, doesn't generalize past X, requires connectivity, breaks under adversarial input, etc.). This is a lightweight pass — hand off to the `researcher` skill before committing real time to any idea that survives Step 4.

## Step 3 — Generate ideas at constraint intersections, not combinations of trends

The reliable pattern for a real gap: technique A solves problem P but fails under constraint C; technique B handles constraint C but doesn't solve P; nobody has combined them because the combination is non-obvious, not because it's easy and just unattempted. Look specifically for:
- A solved problem that breaks the moment a *specific* real-world constraint from Step 1 is added (offline, adversarial, low-power, small-data, real-time).
- A known technique whose limitation is usually "solved" by throwing out a constraint the user's domain can't actually drop.
- A place where two adjacent fields each have half the solution and nobody's connected them (this is the highest-yield pattern for defensible patents).

Avoid: "apply [trendy technique] to [domain]" with no specific mechanism named. If the idea can't be stated as "X handles constraint C by doing [specific mechanism], which Y currently can't because [specific reason]," it's not specific enough yet — push on it.

## Step 4 — Force the "why hasn't this been done" test on every surviving idea

For every candidate, name the most likely reason it doesn't already exist:
- Genuinely hard (technical blocker) — good sign, worth pursuing.
- Nobody needed it until recently (a dependency/market condition just changed) — good sign, worth pursuing, and worth stating what changed.
- Economically not worth it for anyone else, but is worth it here — situational, state why.
- It's actually already been done and the idea generator just didn't know — kill it now, flag for a `researcher` check before the user gets attached to it.
- No real reason — this is a red flag, not a green light. Ideas with no explanation for why they're unclaimed are usually not as novel as they look; say so.

## Output structure

```
# Idea candidates: [domain]

## 1. [Idea name]
- Gap it fills: [specific mechanism vs. specific limitation]
- Why it likely hasn't been done: [reasoned answer from Step 4]
- Feasibility read: [rough — what would have to be true for this to work]
- Next step before committing: [researcher check / patent-novelty-evaluator check / prototype]

(repeat, ranked by conviction — 3 well-reasoned ideas beat 15 generic ones)
```

Don't inflate the list to look productive. If only two ideas survive Step 4, present two — that's the point of the filter.
