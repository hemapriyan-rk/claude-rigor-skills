# Skill Catalog

The full reference for all 30 skills, grouped by function. For each skill you'll find when Claude uses it, the steps it makes Claude follow, and what you get back.

To install skills, see the [README](README.md#install).

---

## 1. Research & Ideation

| Skill | Use when | Core mechanism | Output |
|---|---|---|---|
| [`researcher`](skills/researcher/SKILL.md) | Researching a technical topic, checking prior art, scoping a literature review, or validating a claim before committing to it. Not for quick single-fact lookups. | Scopes the falsifiable question and names the "kill" evidence *before* searching. Searches patents, papers, and shipped products as separate layers — not just the web. Runs a dedicated second pass aimed at finding counter-evidence, not just support. Double-sources every load-bearing claim. | Structured report: question, prior art table, SOTA, strongest counter-evidence found (or how hard it was looked for), sources. |
| [`researcher-evaluator`](skills/researcher-evaluator/SKILL.md) | Given a research output (yours, another AI's, a document) and asked whether it holds up or is safe to act on. | Checklist pass: source quality, recency, coverage of the layer that could falsify the conclusion, cherry-picking, confidence calibration, reproducibility. | Verdict — **Solid / Shaky / Trash** — plus each failure with the specific fix (exact query or source type still missing). Never rounds up. |
| [`idea-finder`](skills/idea-finder/SKILL.md) | Wants new invention/patent/paper/product ideas in a technical space, or direction before committing to a project. | Defines the search space and target artifact first. Generates ideas at constraint intersections (technique A solves P but fails at C; technique B handles C but not P) rather than trend combinations. Forces a "why hasn't this been done" test on every survivor. | Ranked candidate list: gap filled, likely reason it's unclaimed, feasibility read, next step (research/novelty check) — 2-3 solid ideas, not padded volume. |

---

## 2. Patents & IP

| Skill | Use when | Core mechanism | Output |
|---|---|---|---|
| [`patent-novelty-evaluator`](skills/patent-novelty-evaluator/SKILL.md) | Asked "is this patentable," describing an invention/claim, or re-evaluating an existing draft. | Claim skeleton first → prior art search (patents + literature + shipped products) → anticipation test (element-by-element) → obviousness/inventive-step test → subject-matter eligibility check (the real killer for software/AI claims) → claim scope check. | Verdict — **Dead on arrival / Weak-needs narrowing / Defensible** — names the specific closest reference. States plainly it isn't legal advice. |
| [`patent-drafter`](skills/patent-drafter/SKILL.md) | Asked to draft a patent, write claims, or turn an invention into a filing-style document. | Confirms a novelty check happened first (won't silently draft blind). Uses a bundled section-skeleton template (Field, Background, Summary, Detailed Description, Claims, Abstract) with prosecution traps annotated inline — claim breadth tied to the closest prior art found, dependent claims as real fallback positions. | Full draft spec + claim ladder (independent + dependents) + a pre-flight checklist. Explicitly a working draft for attorney review. |
| [`freedom-to-operate-analysis`](skills/freedom-to-operate-analysis/SKILL.md) | Before productizing/commercializing anything patent-adjacent — "can we ship this without infringing." Distinct axis from novelty. | Defines the actual product (not just the claimed invention). Searches for **active, in-force** patents specifically (status matters — expired ≠ risk). Claim-by-claim comparison against every product element, including doctrine-of-equivalents. Flags pending applications as forward risk. | Table of active patents found, classification per hit (**Blocking / Design-around available / Clear**), pending-application watchlist. Explicitly not legal advice. |

---

## 3. Academic Writing

| Skill | Use when | Core mechanism | Output |
|---|---|---|---|
| [`ieee-paper-drafter`](skills/ieee-paper-drafter/SKILL.md) | Writing up a research idea/project/result as an IEEE-format paper, or drafting a specific section (abstract, related work, methodology) in that style. | Bundled ready-to-compile `IEEEtran` LaTeX skeleton with per-section rigor rules inline. Forces Related Work to compare mechanisms (not list citations), baselines to include the real strongest competitor, an explicit Limitations section, every improvement claim tied to a specific metric + baseline. | Full paper draft in IEEE structure/citation style. Recommends running `researcher`/`researcher-evaluator` on Related Work and Results specifically before calling it done. |

---

## 4. Context Handoff

| Skill | Use when | Core mechanism | Output |
|---|---|---|---|
| [`code-handoff`](skills/code-handoff/SKILL.md) | Moving from planning/chat into building — handing a design conversation to Claude Code or a fresh coding session. | Extracts locked decisions, explicitly open items, and **dead ends already ruled out** (the highest-value, most-skipped section) from the conversation, plus environment constraints and testable acceptance criteria. | Paste-ready markdown brief (`TASK.md` shape): locked decisions / open-needs-input / ruled-out approaches / environment / definition of done. |
| [`cross-ai-handoff`](skills/cross-ai-handoff/SKILL.md) | Taking context to a different AI system (ChatGPT, Gemini, a local LLM) with no access to this conversation or Claude's memory. | Strips every self-referential pointer ("as discussed," memory/artifact links). States the receiving model's capability envelope if known. Separates verified fact from Claude's inference. Forces every hedge/caveat from the original to survive compression explicitly. | Self-contained brief: situation, verified facts (sourced), Claude's analysis (marked as such), caveats section, the actual ask. |

---

## 5. System & Infrastructure Design

| Skill | Use when | Core mechanism | Output |
|---|---|---|---|
| [`architecture-design`](skills/architecture-design/SKILL.md) | Designing a new distributed/AI/edge-cloud/agent system, or asked "how should I architect X" for anything with scaling/observability/distributed-state/ML complexity. | Forces explicit numeric non-functional requirements, forces the trade-off decisions to be named (consistency vs. availability, sync/async boundaries, edge/cloud placement) rather than deferred. Mandatory failure-mode analysis and a security/adversarial-ML threat-model pass. Ends with 3 concrete break scenarios. | Full architecture doc: requirements, trade-offs made, component/data-flow diagram (Mermaid), failure modes, threat model, observability, stress-test scenarios. Names the weakest part explicitly. |
| [`architecture-optimization`](skills/architecture-optimization/SKILL.md) | Cost or latency needs to come down on a system that **already works**, without a redesign. Distinct from `architecture-design` (greenfield) and `scale-refactor` (code-level). | Measures actual cost/latency breakdown first. Checks levers in order: caching correctness, right-sizing, data locality, batch-vs-real-time. Checks autoscaling trigger actually correlates with real load. Will flag a service-boundary reconsideration if evidence supports it. | Ranked bottleneck list, lever pulled and why, before/after measurement per change. |
| [`frontend-architecture`](skills/frontend-architecture/SKILL.md) | Architecting a frontend app's structure — not visual styling (a separate, generic visual-design skill covers that). | Rendering strategy (SSR/SSG/ISR/CSR) chosen per-route by requirement. Forces an explicit local/shared/server-state split — the usual root cause of hand-rolled cache-invalidation bugs. Numeric performance budget (bundle size, TTI/LCP). Accessibility treated as a design-time constraint, not a retrofit. | Architecture doc: rendering strategy per section, state boundaries, data-flow pattern, performance budget, accessibility approach. |
| [`database-design`](skills/database-design/SKILL.md) | Designing a new schema, choosing a database technology, or reviewing an existing schema for scaling/correctness issues. | Access-pattern-first (not ERD-first). Every denormalization and every index must tie to a specific listed query — unjustified ones get flagged for removal. SQL vs. NoSQL decided on stated consistency requirement, not fashion. Names the specific cross-shard query pattern that breaks under a chosen shard key. Requires expand-contract migration safety. | Schema design doc with access patterns, indexing rationale, technology choice + consistency model, sharding/replication plan, migration approach. |
| [`api-contract-design`](skills/api-contract-design/SKILL.md) | Designing a new API, reviewing one for breaking-change risk, or adding a field/endpoint to an existing one. | Protocol choice (REST/GraphQL/gRPC) tied to actual requirement, not habit. Forces an explicit versioning + deprecation policy. Error contract designed as first-class (consistent shape, machine-readable codes). Every proposed change classified additive-vs-breaking before shipping. Idempotency stated per mutating operation. | Contract doc: protocol + reasoning, versioning policy, error taxonomy, per-endpoint schema/idempotency/breaking-classification. |
| [`mobile-platform-architecture`](skills/mobile-platform-architecture/SKILL.md) | Architecting a mobile app (iOS/Android/cross-platform) or reviewing one for reliability/battery problems. Distinct from `frontend-architecture` (web-specific). | Offline-first sync strategy and conflict resolution stated explicitly. Designs against real OS background-execution limits (not naive threads). States native/cross-platform bridge boundaries and their serialization cost. Battery/network-awareness as design inputs. Explicit process-death state-restoration plan. Contextual, minimal permission requests. | Architecture doc: offline/sync strategy, background execution plan, bridge boundaries, battery/network behavior, state-restoration plan, permission model. |
| [`agent-system-design`](skills/agent-system-design/SKILL.md) | Designing a new single- or multi-agent AI system, or an existing one is unpredictable, expensive, or hard to debug. Upstream of `ml-security-audit` (which audits code after the fact). | Justifies single- vs. multi-agent choice rather than defaulting to it. Explicit memory/state architecture (short-term/long-term/shared/private). Least-privilege tool allow-list with the prompt-injection seam flagged explicitly. Mandatory runaway/cost guards (iteration cap, budget, timeouts, termination conditions) and a defined escalation path. | Design doc: orchestration justification, memory/state map, tool allow-list, guard specs, escalation path, reasoning-observability approach. |
| [`observability-design`](skills/observability-design/SKILL.md) | Designing observability for a system from scratch, an existing system is "hard to debug in production," or alert fatigue is a stated problem. | SLIs tied to actual user-facing behavior, SLOs and error budgets defined explicitly. Assigns logs/metrics/traces their correct distinct jobs. Trace propagation checked across every async boundary, not just sync calls. Alerts on SLO burn-rate with a hard rule: no runbook, no page. Deliberate cardinality control. | SLI/SLO table, pillar assignment, tracing-boundary map, alerting policy table, dashboard structure (top-down incident path). |

---

## 6. Code Quality, Security & Performance

| Skill | Use when | Core mechanism | Output |
|---|---|---|---|
| [`secure-code-review`](skills/secure-code-review/SKILL.md) | Before merging anything crossing a trust boundary, or asked for a code/security review. | Reads the whole diff for invariants before judging lines in isolation. Checks trust boundaries, internal service-to-service auth (the "it's internal, it's fine" assumption), race/TOCTOU patterns, injection sinks, swallowed security-relevant errors, secrets, fail-open defaults. | Findings ranked by exploitability (Critical→Low), each with the concrete exploit scenario and fix — not a style-nitpick wall. |
| [`ml-security-audit`](skills/ml-security-audit/SKILL.md) | Any inference pipeline, training loop, LLM agent with tool access, or sensor-fusion/vision code, before treating it as production-ready. Distinct from general security review. | Maps every point where attacker-influenced data reaches a model. Checks evasion (confidence thresholding + defined fallback), poisoning (retrain-on-live-data provenance), model/IP extraction (rate-limiting, on-device extractability), prompt injection (trusted-instruction/untrusted-data separation), sensor spoofing (cross-sensor consistency). | Findings by attack class: surface, exploit scenario, current mitigation, fix — only for classes actually reachable given the real data flow. |
| [`crypto-storage-audit`](skills/crypto-storage-audit/SKILL.md) | Any code handling encryption keys, an encrypted file format, or policy-gated decryption logic. | Checks in order of real-world frequency: hand-rolled primitives (automatic top severity), nonce/IV reuse, DEK/KEK hierarchy correctness, whether the policy gate is enforced at the actual decrypt call site (not a bypassable UI layer), timing side-channels, key rotation/revocation actually invalidating old access, secure-deletion completeness. | Findings by class, each with location/what's-wrong/why-it-matters/fix. Hand-rolled crypto or confirmed nonce reuse always surfaces first. |
| [`distributed-debugger`](skills/distributed-debugger/SKILL.md) | A bug is intermittent, hard to reproduce, only shows under load, or spans services. Not for deterministic bugs. | Forces a reliable reproduction before any fix attempt. Isolates the smallest failing case. Checks concurrency-specific suspects explicitly: shared-state races, check-then-act, non-idempotent retries, cross-boundary ordering assumptions, retry-storm-causing timeouts, clock skew. Re-verifies the fix against a harder version of the original reproduction. | Root cause (mechanism, not symptom), smallest repro, fix, and how the fix was verified. |
| [`test-architect`](skills/test-architect/SKILL.md) | Asked to write tests, or code touches concurrency/external I/O/network/ML inference and needs real confidence. | Targets boundary values, plausible-malformed input, concurrent access patterns, per-dependency failure injection (timeout/error/partial response), and — for ML — out-of-distribution/low-confidence paths. Prioritizes a regression test for any known real bug. Explicitly refuses to count happy-path variants as coverage. | Tests mapped one-to-one to a named risk each covers — count of distinct risks covered, not test count. |
| [`scale-refactor`](skills/scale-refactor/SKILL.md) | A working prototype/PoC needs to survive real load, real failures, or a real audit, without a full rewrite. | Ranks scaling assumptions by which breaks first (single-instance state, unbounded queues, sync bottlenecks, no backpressure) — not all fixed equally. Adds observability at the actual identified failure points. Opportunistically hardens trust boundaries while the code is already open. Tracks what was deliberately left untouched. | Ranked bottleneck list, what changed and why, observability added, explicit list of what was left alone. |
| [`performance-optimization`](skills/performance-optimization/SKILL.md) | Something needs to be faster, or the user reports something as slow. Refuses to justify guessing at what's slow. | Measures (profiles) before any change. Identifies bottleneck class (CPU/I-O/memory-bound) before picking a fix direction. Fixes in leverage order: algorithmic complexity → data structure → micro-optimization. Explicitly guards against optimizing off the critical path. Re-verifies with the same measurement on the user-facing metric, not a proxy. | Bottleneck (with profile evidence), fix applied and why over alternatives, before/after measurement from the same method. |
| [`embedded-constrained-coding`](skills/embedded-constrained-coding/SKILL.md) | Target is a microcontroller, on-device mobile/edge inference, or any hard memory/power/latency ceiling. Not for ordinary server code. | Forces the actual RAM/flash/power/latency budget to be stated as numbers before writing code. Flags heap-fragmenting allocation patterns, blocking calls in real-time paths, watchdog-timer risk. Requires quantization/precision tradeoffs to be measured, not assumed. Requires the final result to be verified against the budget, not estimated. | Budget stated, what was done to fit it, what was measured vs. only estimated (flagged explicitly). |

---

## 7. ML Engineering

| Skill | Use when | Core mechanism | Output |
|---|---|---|---|
| [`ml-model-selection`](skills/ml-model-selection/SKILL.md) | Picking a model for a new pipeline, or reconsidering one that's too slow/expensive/large for its deployment target. | Constraints stated as numbers first (latency/accuracy/compute/deployment target). Explicitly resists defaulting to the largest/newest model — treats "clears the floor by far more than needed" as wasted budget, not safety margin. Considers classical/distilled baselines as real candidates. Requires quantization impact to be measured. Evaluates against the real deployment distribution, not the model's famous benchmark. | 2-3 candidates with a real trade-off table (accuracy/latency/memory/cost), recommendation with the specific reason runner-ups were rejected. |
| [`dataset-sourcing`](skills/dataset-sourcing/SKILL.md) | A project needs training/validation data, before treating any found dataset as ready-to-use. | Defines the real deployment distribution first as the acceptance criteria. Searches domain/adjacent/collect-instead layers. Checks license before anything else. Checks train/test leakage, label noise, shortcut-artifact risk. Compares distribution match against the real deployment domain explicitly. Checks representation gaps for safety/identity-relevant domains. | Dataset shortlist table (license/size/distribution-match/known gaps) plus an explicit usable-as-is / needs-augmentation / collect-instead verdict. |

---

## 8. Compliance

| Skill | Use when | Core mechanism | Output |
|---|---|---|---|
| [`safety-compliance-scoping`](skills/safety-compliance-scoping/SKILL.md) | A system's use case touches health, safety, or regulated industrial contexts — early, before deep technical/product investment. | Classifies actual use case and failure consequence first (this decides everything downstream). Names only plausibly-relevant frameworks (functional safety standards, device-classification pathways, industrial directives) rather than an exhaustive list. States each framework's requirement burden at scoping depth. Flags the earliest points where a late risk-classification forces expensive rework. | Table: candidate frameworks, why each might apply, requirement burden, earliest affected decision points. Explicitly a scoping map, not a certification — states a compliance professional/legal counsel must own the real path. |

---

## 9. Dev Workflow

| Skill | Use when | Core mechanism | Output |
|---|---|---|---|
| [`github-master`](skills/github-master/SKILL.md) | Setting up git/GitHub for a project, wanting work checkpointed/committed automatically, pushing/pulling/syncing with a remote, or deciding a branching strategy. | Bundles a `scripts/checkpoint.sh` (local-only, stages+commits, no-op on a clean tree). Defaults new remotes to **private**; treats repo creation and first push as confirm-before-acting. Checkpoints stay local and `checkpoint:`-prefixed unless the user explicitly wants them pushed. Enforces fetch-before-push always; force-push only with `--force-with-lease` on a branch that's exclusively the user's own. Surfaces local/remote divergence explicitly rather than silently resolving it. | Connected remote, disciplined checkpoint history, clean commit messages, safe sync — with every remote-affecting or history-rewriting action confirmed rather than automated silently. |
| [`project-scaffolding`](skills/project-scaffolding/SKILL.md) | Starting a new project/repo, adding a module needing its own structural convention, or restructuring a messy existing layout. | Identifies actual project type first (library/app/service/monorepo each need a different layout). Follows the ecosystem's real convention and states which one — never an invented ad hoc structure. Separates source/tests/config/build/docs cleanly. Minimum-viable boilerplate only — no empty "future use" folders. States monorepo package boundaries explicitly. Treats restructuring as a stated migration (`git mv`), not a silent rewrite. | Directory tree created, convention followed and why, and which parts are functional immediately vs. placeholders. |

---

## Cross-references worth knowing

Several skills are designed to chain into each other rather than duplicate coverage:

- `researcher` → `researcher-evaluator` (produce, then stress-test)
- `idea-finder` → `researcher` / `patent-novelty-evaluator` (before committing time to a candidate idea)
- `patent-novelty-evaluator` → `patent-drafter` (novelty check gates drafting) → `freedom-to-operate-analysis` (separate axis, before commercializing)
- `architecture-design` (greenfield) vs. `architecture-optimization` (existing system) vs. `scale-refactor` (code-level, not infra-level)
- `agent-system-design` (upstream design) → `ml-security-audit` (audits the resulting code's injection seam)
- `embedded-constrained-coding` ↔ `ml-model-selection` (shared budget numbers)
- `dataset-sourcing` ↔ `ml-model-selection` (shared distribution-match discipline)
- `secure-code-review` / `crypto-storage-audit` ↔ `github-master` (secret-check before commit)
- `code-handoff` (Claude → Claude Code) vs. `cross-ai-handoff` (Claude → any other model) — different failure modes, don't conflate

---

*None of the skills refer to a specific project. All examples are generic.*
