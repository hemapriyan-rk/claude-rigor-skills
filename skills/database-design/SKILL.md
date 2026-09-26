---
name: database-design
description: Design a database schema and storage strategy — normalization vs. denormalization, indexing, SQL vs. NoSQL choice, sharding/replication and consistency model — with every trade-off stated explicitly rather than defaulted by habit or fashion. Use when designing a new schema, choosing a database technology, or reviewing an existing schema for scaling or correctness issues.
---

# Database Design

A schema designed from the entity-relationship diagram alone is designed from the wrong input. The ERD describes the domain; the actual read/write access pattern is what should drive the schema, indexing, and technology choice.

## Step 1 — Access pattern first

Before drawing tables, list the actual queries this schema needs to serve well: what's read together, what's written together, what's queried by range vs. exact match, what needs to be fast versus what can be slow. Design from this list, not from the domain model in isolation.

## Step 2 — Normalization vs. denormalization, with a stated reason

Every denormalized table needs an explicit reason tied to Step 1 (a specific hot query that needs the data pre-joined). Denormalization with no stated reason is pure inconsistency risk with no offsetting benefit — flag it as a problem, not a style choice, when found without justification.

## Step 3 — SQL vs. NoSQL as a real trade-off

Decide based on the actual consistency requirement (strong vs. eventual — state this explicitly) and query flexibility need from Step 1, not team familiarity or what's trending. A document store chosen for a workload that's actually relational (many cross-entity joins in the access pattern) creates exactly the joins-in-application-code problem the choice was supposed to avoid.

## Step 4 — Indexing tied to the access pattern

Every index has a write-cost — only add one that serves a query actually in the Step 1 list. Check specifically for:
- Missing indexes on foreign keys / join columns that Step 1's queries actually hit.
- Indexes added "just in case" that serve no listed query — these slow every write for no read benefit and should be flagged for removal, not just left alone.

## Step 5 — Sharding, replication, and consistency model

If scaling past a single node: state the shard key and name the cross-shard query pattern it breaks — there is always at least one, and pretending otherwise just defers the discovery to an incident. For read replicas, state the acceptable replication lag explicitly if any read path can tolerate staleness, and flag any read path that can't but is routed to a replica anyway.

## Step 6 — Migration safety

Check that schema migrations are backward-compatible with currently-running code during rollout (expand-contract: add the new column/table first, migrate reads, then remove the old one in a later deploy) rather than a hard cutover that breaks any instance still running the old code mid-deploy.

## Output

```
# Database design: [system]
## Access patterns (the queries this must serve well)
## Schema (with denormalization decisions and their stated reason)
## Technology choice (SQL/NoSQL) and the consistency model that drove it
## Indexes (each tied to a specific query) and any flagged as unjustified
## Sharding/replication strategy, with the cross-shard query pattern that breaks named explicitly
## Migration approach
```
