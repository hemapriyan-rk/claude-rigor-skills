---
name: api-contract-design
description: Design the contract between services or between client and server — protocol choice (REST/GraphQL/gRPC), versioning strategy, error-response contract, and backward-compatibility rules. Use whenever designing a new API, reviewing one for a breaking-change risk, or asked to add a field/endpoint to an existing API. Sits between database design and frontend/client design — the boundary contract itself, not either side's internals.
---

# API Contract Design

Most API problems that look like "the frontend and backend disagree" are actually a contract that was never made explicit, and both sides guessed compatibly for a while until they didn't. This skill makes the contract explicit before code on either side depends on an assumption.

## Step 1 — Choose the protocol by requirement, not habit

- **REST** — resource-oriented access with good cacheability, when the access pattern maps cleanly to a fixed set of resources and standard HTTP semantics fit.
- **GraphQL** — when clients genuinely need flexible, partial data shapes and over-fetching/under-fetching with a fixed REST shape is a real, current problem — not by default because it's more flexible in theory.
- **gRPC** — for internal service-to-service calls where performance, strong typing, and/or streaming matter more than human-readability or broad client compatibility.
State the actual reason for the choice — "REST because that's what we always use" is not a decision, it's an unexamined default.

## Step 2 — Decide versioning strategy up front

URI versioning, header versioning, or schema evolution via additive-only changes — pick one and state the deprecation policy alongside it: how long old versions stay supported, and how consumers are notified before a version is retired. A versioning strategy decided after the first breaking change is needed is a strategy decided too late.

## Step 3 — Design the error contract as a first-class part of the API

A consistent error shape across every endpoint, with machine-readable error codes separate from human-readable messages (clients should branch on the code, not parse the message string). Keep client-error and server-error semantics distinct and consistent regardless of transport, so callers can reliably distinguish "you sent something wrong" from "we failed, retry might help."

## Step 4 — Classify every change as additive or breaking, explicitly

Additive changes (a new optional field, a new endpoint) are safe without a version bump. Removing or renaming a field, changing a field's type, or changing existing behavior is breaking and requires either a version bump or a formal deprecation cycle. Before shipping any API change, state which category it falls into — this single habit prevents most accidental breaking changes that "seemed small."

## Step 5 — State idempotency explicitly for every mutating operation

Retries are a fact of life in any distributed system — a client or a network layer will eventually retry a request that actually succeeded. State explicitly which operations are idempotent and by what mechanism (an idempotency key, or a naturally idempotent operation like "set to value X" versus "increment by 1"). An operation with no stated idempotency behavior will eventually double-apply somewhere.

## Output

```
# API contract: [service/boundary]
## Protocol choice and why
## Versioning strategy + deprecation policy
## Error contract (shape, code taxonomy)
## Endpoints: method, request/response schema, idempotency, and whether each is additive or breaking relative to the prior contract
```
