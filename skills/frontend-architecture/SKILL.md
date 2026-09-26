---
name: frontend-architecture
description: Design frontend architecture — rendering strategy (SSR/SSG/ISR/CSR), state management boundaries, component data flow, and performance budgets — as structural/technical decisions, not visual styling. Use when architecting a new frontend app or reviewing an existing one for state-management or rendering-strategy problems. This is not about aesthetics, layout, or typography — use the visual design skill for that; this skill is about where state lives and how data flows.
---

# Frontend Architecture

Most frontend architecture problems aren't visual — they're state living in the wrong place, or a rendering strategy picked by habit instead of by the actual requirement. This skill forces both decisions explicitly.

## Step 1 — Rendering strategy, chosen by requirement, not default

Pick SSR/SSG/ISR/CSR based on the actual needs: does this route need SEO (rules out pure CSR), does content update per-request or can it be built ahead of time (SSG/ISR) or does it need per-request personalization (SSR/CSR)? A team defaulting to one strategy across an entire app regardless of per-route requirements is a common, avoidable cost.

## Step 2 — State management boundaries, stated explicitly

Separate three categories and say which is which for the app being designed:
- **Local component state** — belongs to one component, doesn't need to escape it.
- **Shared app state** — genuinely needs to be read/written from multiple, unrelated parts of the tree.
- **Server state (cache)** — data that actually lives on a server and is being cached client-side.

The most common frontend architecture failure is treating server data as if it were client app state — teams end up hand-rolling cache invalidation, staleness, and refetch logic that a dedicated server-state library already solves. If the app doesn't clearly separate these, that's the finding to raise first, before any component-level review.

## Step 3 — Component data flow

State the direction data flows and how: prop drilling for shallow trees, context for broadly-needed low-frequency-change data, a state library for high-frequency shared state. Distinguish presentational ("dumb") components from stateful containers, and check the boundary is actually where it's claimed to be — a "presentational" component reaching into global state directly is a sign the boundary has already eroded.

## Step 4 — Performance budget, as numbers

State explicit targets: bundle size ceiling, Time-to-Interactive/Largest-Contentful-Paint targets. Decide what's code-split versus eagerly loaded based on those numbers, not on "it feels big." A budget nobody measured against isn't a budget.

## Step 5 — Accessibility as a first-class constraint

Check semantic structure and keyboard/screen-reader navigation at design time — retrofitting accessibility after the component tree is built is far more expensive and usually incomplete. This isn't a separate audit pass; it's part of the same architecture decision as Step 3.

## Output

```
# Frontend architecture: [app/feature]
## Rendering strategy per route/section, and why
## State boundaries (local / shared / server-cache) — explicit
## Component data-flow pattern and where the presentational/stateful boundary sits
## Performance budget (numbers) and what's code-split
## Accessibility approach
```
