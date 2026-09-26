# claude-rigor-skills

**Claude Code skills for engineering, research, and patent work where a plausible answer isn't good enough.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Skills: 30](https://img.shields.io/badge/skills-30-informational)
![Claude Code](https://img.shields.io/badge/Claude%20Code-skills-d97757)

Each skill makes Claude do the step that usually gets skipped: state the budget before writing embedded code, search for the prior art that would kill a patent claim, name the query a shard key breaks, profile before optimizing, and give a blunt verdict instead of reassurance.

---

## Contents

- [Install](#install)
- [Pick only what you need](#pick-only-what-you-need)
- [Skills](#skills)
- [How the skills work together](#how-the-skills-work-together)
- [Good to know](#good-to-know)
- [Update or remove](#update-or-remove)
- [License](#license)

---

## Install

### Option 1: Ask Claude (recommended)

Paste this into Claude Code:

```text
Install skills from https://github.com/hemapriyan-rk/claude-rigor-skills.
Follow the INSTALL.md in that repo.
```

Claude asks what you work on, suggests a set of skills that fits, checks for conflicts with skills you already have, and installs only the ones you approve. The steps it follows are in [INSTALL.md](INSTALL.md).

### Option 2: Install manually

```sh
git clone --depth 1 https://github.com/hemapriyan-rk/claude-rigor-skills.git
```

Copy the skill folders you want from `skills/` into your skills directory:

| Scope | Directory |
|---|---|
| All your projects | `~/.claude/skills/` |
| One project only | `.claude/skills/` in the project root |

**macOS / Linux:**

```sh
for s in secure-code-review test-architect github-master; do
  cp -r claude-rigor-skills/skills/$s ~/.claude/skills/
done
```

**Windows (PowerShell):**

```powershell
foreach ($s in "secure-code-review", "test-architect", "github-master") {
  Copy-Item -Recurse "claude-rigor-skills\skills\$s" "$HOME\.claude\skills\"
}
```

Start a new Claude Code session afterwards. Claude uses a skill automatically when your request matches its description, and you can also ask for one by name: *"use the patent-novelty-evaluator skill on this."*

---

## Pick only what you need

> [!WARNING]
> **Don't install all 30 skills unless you really use all of them.**
>
> - **Unneeded skills get in the way.** Claude loads every installed skill's description and uses it to decide which skill to apply. Skills for work you never do can trigger on requests where you just wanted a quick answer. For example, a research skill might start a multi-source search.
> - **Similar skills compete.** The more skills you install that cover the same area, the less predictable Claude's choice becomes.
> - **Don't install duplicates.** If you already have some of these skills from claude.ai or another source, don't install them again.
>
> Start with a bundle below. You can always add more later.

### Starter bundles

| You work on… | Start with |
|---|---|
| **Any software project** | `github-master` · `project-scaffolding` · `code-handoff` |
| **Backend and distributed systems** | `architecture-design` · `api-contract-design` · `database-design` · `observability-design` · `distributed-debugger` · `performance-optimization` · `test-architect` |
| **Frontend and mobile** | `frontend-architecture` · `mobile-platform-architecture` · `api-contract-design` · `performance-optimization` · `test-architect` |
| **Prototype to production** | `scale-refactor` · `architecture-optimization` · `observability-design` · `secure-code-review` · `test-architect` |
| **Security** | `secure-code-review` · `crypto-storage-audit` · `ml-security-audit` |
| **ML and AI engineering** | `ml-model-selection` · `dataset-sourcing` · `ml-security-audit` · `agent-system-design` |
| **Embedded and edge** | `embedded-constrained-coding` · `ml-model-selection` · `performance-optimization` |
| **Research and papers** | `researcher` · `researcher-evaluator` · `idea-finder` · `ieee-paper-drafter` |
| **Patents and IP** | `patent-novelty-evaluator` · `patent-drafter` · `freedom-to-operate-analysis` · `researcher` |

---

## Skills

One line per skill. For when each one applies, the steps it follows, and what it produces, see the **[full catalog in SKILLS.md](SKILLS.md)**.

### Research and ideation

| Skill | What it does |
|---|---|
| [`researcher`](skills/researcher/SKILL.md) | Researches across papers, patents, shipped products, and standards, and searches for counter-evidence, not just support. |
| [`researcher-evaluator`](skills/researcher-evaluator/SKILL.md) | Checks a piece of research for rigor and gives a verdict: solid, shaky, or trash. |
| [`idea-finder`](skills/idea-finder/SKILL.md) | Finds gaps where known techniques each fail, and drops ideas that can't explain why nobody has built them. |

### Patents and IP

| Skill | What it does |
|---|---|
| [`patent-novelty-evaluator`](skills/patent-novelty-evaluator/SKILL.md) | Tests novelty, obviousness, and eligibility against the closest prior art. Verdict: dead, weak, or defensible. |
| [`patent-drafter`](skills/patent-drafter/SKILL.md) | Drafts a full specification and claim ladder from a template, after a novelty check. |
| [`freedom-to-operate-analysis`](skills/freedom-to-operate-analysis/SKILL.md) | Checks whether shipping a product would infringe active patents, claim by claim. |

### Academic writing

| Skill | What it does |
|---|---|
| [`ieee-paper-drafter`](skills/ieee-paper-drafter/SKILL.md) | Drafts an IEEE-format paper from a LaTeX template, holding each section to reviewer-level rules. |

### Context handoff

| Skill | What it does |
|---|---|
| [`code-handoff`](skills/code-handoff/SKILL.md) | Turns a planning chat into a brief for a coding agent: locked decisions, open items, approaches already ruled out. |
| [`cross-ai-handoff`](skills/cross-ai-handoff/SKILL.md) | Writes a brief another AI can use without this chat's context, keeping facts, inferences, and caveats separate. |

### System and infrastructure design

| Skill | What it does |
|---|---|
| [`architecture-design`](skills/architecture-design/SKILL.md) | Designs a system with explicit trade-offs, failure modes, a threat model, and break scenarios. |
| [`architecture-optimization`](skills/architecture-optimization/SKILL.md) | Cuts cost or latency on a working system, measuring before and after each change. |
| [`frontend-architecture`](skills/frontend-architecture/SKILL.md) | Picks a rendering strategy per route and sets state boundaries and performance budgets. |
| [`database-design`](skills/database-design/SKILL.md) | Designs schema, indexes, and sharding from how the data is actually read and written. |
| [`api-contract-design`](skills/api-contract-design/SKILL.md) | Sets the protocol, versioning, error contract, idempotency, and rules for breaking changes. |
| [`mobile-platform-architecture`](skills/mobile-platform-architecture/SKILL.md) | Covers offline sync, background limits, the app being killed in the background, battery, and permissions. |
| [`agent-system-design`](skills/agent-system-design/SKILL.md) | Designs agent orchestration, memory, least-privilege tool access, and limits on runaway loops and cost. |
| [`observability-design`](skills/observability-design/SKILL.md) | Defines SLIs/SLOs, trace propagation, label cardinality, and alerts that stay actionable. |

### Code quality, security, and performance

| Skill | What it does |
|---|---|
| [`secure-code-review`](skills/secure-code-review/SKILL.md) | Reviews code for security and correctness bugs, ranked by how exploitable they are, not by style. |
| [`ml-security-audit`](skills/ml-security-audit/SKILL.md) | Audits for evasion, poisoning, model extraction, prompt injection, and sensor spoofing. |
| [`crypto-storage-audit`](skills/crypto-storage-audit/SKILL.md) | Audits key handling, nonce reuse, where access checks are enforced, and whether deleted data is really gone. |
| [`distributed-debugger`](skills/distributed-debugger/SKILL.md) | Finds the root cause of races, deadlocks, and retry storms. Reproduces the bug before fixing it. |
| [`test-architect`](skills/test-architect/SKILL.md) | Writes tests for edge cases, concurrency, and dependency failures, each tied to a named risk. |
| [`scale-refactor`](skills/scale-refactor/SKILL.md) | Takes a working prototype toward production without a rewrite. |
| [`performance-optimization`](skills/performance-optimization/SKILL.md) | Profiles first, fixes the algorithm before micro-optimizing, and re-measures the same way. |
| [`embedded-constrained-coding`](skills/embedded-constrained-coding/SKILL.md) | Writes code to a stated RAM, flash, power, and latency budget, and measures against it. |

### ML engineering

| Skill | What it does |
|---|---|
| [`ml-model-selection`](skills/ml-model-selection/SKILL.md) | Picks a model within latency, accuracy, and compute budgets instead of defaulting to the biggest. |
| [`dataset-sourcing`](skills/dataset-sourcing/SKILL.md) | Checks datasets for license, leakage, bias, and match with real deployment data. |

### Compliance

| Skill | What it does |
|---|---|
| [`safety-compliance-scoping`](skills/safety-compliance-scoping/SKILL.md) | Maps which safety and regulatory frameworks apply before the architecture is locked in. |

### Dev workflow

| Skill | What it does |
|---|---|
| [`github-master`](skills/github-master/SKILL.md) | Connects repos to GitHub, makes local checkpoint commits, writes clear commit messages, and syncs safely. |
| [`project-scaffolding`](skills/project-scaffolding/SKILL.md) | Lays out new projects the way their ecosystem expects, with no empty placeholder folders. |

---

## How the skills work together

Several skills are built to run one after another:

```text
idea-finder ──► researcher ──► researcher-evaluator
                    │
patent-novelty-evaluator ──► patent-drafter ──► freedom-to-operate-analysis

agent-system-design ──► ml-security-audit
```

- **Choose one of three:** use `architecture-design` for a new system, `architecture-optimization` to make an existing system cheaper or faster, and `scale-refactor` to change code rather than infrastructure.
- **Pairs that share the same checks:** `ml-model-selection` works with `embedded-constrained-coding` (the same hardware budget) and `dataset-sourcing` (the same test against real deployment data).
- **Handoffs:** use `code-handoff` to hand work to a coding agent, and `cross-ai-handoff` to take it to a different AI.

Each skill works on its own. The partners above make it stronger.

---

## Good to know

- **`github-master` commits for you, locally.** It makes `checkpoint:` commits during work but never pushes, force-pushes, or creates a repo without asking. New repos default to private.
- **Research-heavy skills take longer.** `researcher`, `patent-novelty-evaluator`, `freedom-to-operate-analysis`, and `dataset-sourcing` run many searches before answering. That's deliberate.
- **Not legal advice.** `patent-novelty-evaluator`, `patent-drafter`, `freedom-to-operate-analysis`, and `safety-compliance-scoping` produce technical analysis and working drafts. Have a patent attorney or qualified compliance professional review anything before you file or make a compliance claim.
- **Blunt by design.** Several skills give verdicts like *dead on arrival* or *trash*. They're meant to catch problems before a reviewer, examiner, or production incident does.

---

## Update or remove

- **Update:** pull the latest version of the repo and copy the skill folders again.
- **Remove:** delete the skill's folder from `~/.claude/skills/` (or `.claude/skills/`) and start a new session.

---

## License

[MIT](LICENSE). Use them, change them, and share them.
