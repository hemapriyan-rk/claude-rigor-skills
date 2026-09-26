<div align="center">

# claude-rigor-skills

**30 Claude Code skills that make AI engineering and research less hand-wavy.**

Security reviews, architecture, performance, testing, ML, research, and patents, each with explicit checks for budgets, failure modes, and evidence.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Skills: 30](https://img.shields.io/badge/skills-30-informational)](SKILLS.md)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-skills-d97757)](https://docs.claude.com/en/docs/claude-code)
[![Consistency check](https://github.com/hemapriyan-rk/claude-rigor-skills/actions/workflows/check.yml/badge.svg)](.github/workflows/check.yml)

</div>

---

## Try it in 30 seconds

Paste this into Claude Code:

```text
Install skills from https://github.com/hemapriyan-rk/claude-rigor-skills.
Follow the INSTALL.md in that repo.
```

Claude asks what you work on, suggests the skills that fit, checks for skills you already have, and installs only the ones you approve. [Manual install](#manual-install) is below.

---

## Why this exists

### AI is good at producing answers. These skills make it show its work.

A plausible answer is easy to get and expensive to act on. Each skill makes Claude do the step that usually gets skipped:

| Instead of… | The skill makes Claude… |
|---|---|
| "This design should scale" | name the trade-offs, list the failure modes, and run three break scenarios (`architecture-design`) |
| "It's probably the loop" | profile first, then re-measure with the same method (`performance-optimization`) |
| "Looks secure to me" | rank findings by how exploitable they are, each with a concrete attack path (`secure-code-review`) |
| "This invention sounds novel" | find the closest prior art and give a verdict: dead, weak, or defensible (`patent-novelty-evaluator`) |
| "Should fit on the device" | state the RAM, flash, and power budget, and measure against it (`embedded-constrained-coding`) |
| "Here are 15 tests" | map each test to a named risk: concurrency, dependency failure, malformed input (`test-architect`) |

Several skills give blunt verdicts on purpose. They're meant to catch problems before a reviewer, patent examiner, or production incident does.

---

## What's inside

| | Category | Skills |
|---|---|---|
| 🔐 | **Security** | [`secure-code-review`](skills/secure-code-review/SKILL.md) · [`ml-security-audit`](skills/ml-security-audit/SKILL.md) · [`crypto-storage-audit`](skills/crypto-storage-audit/SKILL.md) |
| 🏗️ | **Architecture** | [`architecture-design`](skills/architecture-design/SKILL.md) · [`architecture-optimization`](skills/architecture-optimization/SKILL.md) · [`api-contract-design`](skills/api-contract-design/SKILL.md) · [`database-design`](skills/database-design/SKILL.md) · [`frontend-architecture`](skills/frontend-architecture/SKILL.md) · [`mobile-platform-architecture`](skills/mobile-platform-architecture/SKILL.md) · [`agent-system-design`](skills/agent-system-design/SKILL.md) · [`observability-design`](skills/observability-design/SKILL.md) |
| 🧪 | **Quality and performance** | [`test-architect`](skills/test-architect/SKILL.md) · [`distributed-debugger`](skills/distributed-debugger/SKILL.md) · [`performance-optimization`](skills/performance-optimization/SKILL.md) · [`scale-refactor`](skills/scale-refactor/SKILL.md) · [`embedded-constrained-coding`](skills/embedded-constrained-coding/SKILL.md) |
| 🤖 | **ML engineering** | [`ml-model-selection`](skills/ml-model-selection/SKILL.md) · [`dataset-sourcing`](skills/dataset-sourcing/SKILL.md) |
| 🔬 | **Research** | [`researcher`](skills/researcher/SKILL.md) · [`researcher-evaluator`](skills/researcher-evaluator/SKILL.md) · [`idea-finder`](skills/idea-finder/SKILL.md) · [`ieee-paper-drafter`](skills/ieee-paper-drafter/SKILL.md) |
| 📜 | **Patents and compliance** | [`patent-novelty-evaluator`](skills/patent-novelty-evaluator/SKILL.md) · [`patent-drafter`](skills/patent-drafter/SKILL.md) · [`freedom-to-operate-analysis`](skills/freedom-to-operate-analysis/SKILL.md) · [`safety-compliance-scoping`](skills/safety-compliance-scoping/SKILL.md) |
| 🛠️ | **Dev workflow** | [`github-master`](skills/github-master/SKILL.md) · [`project-scaffolding`](skills/project-scaffolding/SKILL.md) · [`code-handoff`](skills/code-handoff/SKILL.md) · [`cross-ai-handoff`](skills/cross-ai-handoff/SKILL.md) |

**[→ Full catalog (SKILLS.md)](SKILLS.md):** when each skill applies, the steps it follows, and what it produces.

---

## Pick only what you need

> [!WARNING]
> **Don't install all 30 skills unless you really use all of them.**
>
> - **Unneeded skills get in the way.** Claude reads every installed skill's description to decide which one to apply. Skills for work you never do can trigger on requests where you just wanted a quick answer.
> - **Similar skills compete.** The more skills you have covering the same area, the less predictable Claude's choice becomes.
> - **Don't install duplicates.** If you already have some of these skills from claude.ai or another source, don't install them again.
>
> Start with a bundle below. You can always add more later.

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

## Manual install

```sh
git clone --depth 1 https://github.com/hemapriyan-rk/claude-rigor-skills.git
```

Copy the skill folders you want from `skills/` into `~/.claude/skills/` (all projects) or `.claude/skills/` in a project root (that project only).

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

**Update:** pull the repo and copy the folders again. **Remove:** delete the skill's folder and start a new session.

---

## How the skills work together

```text
idea-finder ──► researcher ──► researcher-evaluator
                    │
patent-novelty-evaluator ──► patent-drafter ──► freedom-to-operate-analysis

agent-system-design ──► ml-security-audit
```

- **Choose one of three:** `architecture-design` for a new system, `architecture-optimization` to make an existing one cheaper or faster, and `scale-refactor` to change code rather than infrastructure.
- **Pairs that share the same checks:** `ml-model-selection` works with `embedded-constrained-coding` (the same hardware budget) and `dataset-sourcing` (the same test against real deployment data).

Each skill works on its own. The partners make it stronger.

---

## Good to know

- **`github-master` commits for you, locally.** It makes `checkpoint:` commits during work but never pushes, force-pushes, or creates a repo without asking.
- **Research-heavy skills take longer.** `researcher`, `patent-novelty-evaluator`, `freedom-to-operate-analysis`, and `dataset-sourcing` run many searches before answering.
- **Not legal advice.** The patent and compliance skills produce technical analysis and working drafts. Have a patent attorney or qualified compliance professional review anything before you file or make a compliance claim.

---

## License

[MIT](LICENSE). Use them, change them, and share them.
