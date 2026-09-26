# Install guide for Claude

This file is written for Claude Code. When a user asks you to install skills from this repository, follow these steps in order. The goal is to install **the skills this user will actually use**, not all 30.

## 1. Find out what the user works on

Unless the user already named the skills they want, ask one short question about their work. For example:

> What kind of work do you mostly use Claude for? For example: backend services, frontend or mobile apps, ML, security, research papers, patents, or something else.

Don't send the user a list of 30 skills and ask them to pick.

## 2. Recommend a set

Start from the matching bundle or bundles below, then adjust to what the user told you. Aim for about 5–10 skills. If they name specific skills, install exactly those.

| If the user does… | Recommend |
|---|---|
| Any software work (core) | `github-master`, `project-scaffolding`, `code-handoff` |
| Backend or distributed systems | `architecture-design`, `api-contract-design`, `database-design`, `observability-design`, `distributed-debugger`, `performance-optimization`, `test-architect` |
| Frontend or mobile | `frontend-architecture`, `mobile-platform-architecture`, `api-contract-design`, `performance-optimization`, `test-architect` |
| Taking a prototype to production | `scale-refactor`, `architecture-optimization`, `observability-design`, `secure-code-review`, `test-architect` |
| Security | `secure-code-review`, `crypto-storage-audit`, `ml-security-audit` |
| ML or AI engineering | `ml-model-selection`, `dataset-sourcing`, `ml-security-audit`, `agent-system-design` |
| Embedded, edge, or on-device | `embedded-constrained-coding`, `ml-model-selection`, `performance-optimization` |
| Research or academic writing | `researcher`, `researcher-evaluator`, `idea-finder`, `ieee-paper-drafter` |
| Patents or inventions | `patent-novelty-evaluator`, `patent-drafter`, `freedom-to-operate-analysis`, `researcher` |
| Health, safety, or regulated products | `safety-compliance-scoping` |
| Moving work to another AI tool | `cross-ai-handoff` |

Some skills hand off to others. If you recommend one of these, suggest its partner too:

- `patent-drafter` expects `patent-novelty-evaluator` to have run first.
- `ieee-paper-drafter` and `idea-finder` call on `researcher` and `researcher-evaluator`.
- `researcher` hands its output to `researcher-evaluator`.

Each skill's `description` field in `skills/<name>/SKILL.md` says when it applies. [SKILLS.md](SKILLS.md) has the full catalog.

## 3. Mention what to know before installing

Tell the user these points briefly, and only the ones that apply to the skills you're recommending:

- **`github-master`** makes local checkpoint commits during work. It never pushes without asking.
- **`researcher`, `patent-novelty-evaluator`, `freedom-to-operate-analysis`, and `dataset-sourcing`** run many web searches, so they're slower than a quick answer.
- **Patent and compliance skills** produce technical analysis, not legal advice.

## 4. Check for conflicts

Before copying anything:

1. List the target directory (see step 5) and check whether a skill with the same name already exists. If one does, show the user and ask whether to replace it. Don't overwrite silently.
2. Check whether the user already has the same skill from another source, such as skills synced from claude.ai (they show up with an `anthropic-skills:` or similar prefix in your skill list). Installing a second copy makes Claude pick between two identical skills, so skip those unless the user wants a local copy.

## 5. Confirm, then install

Show the user the final list and where it will go, and wait for a yes.

- **All projects (default):** `~/.claude/skills/<skill-name>/`
- **This project only:** `.claude/skills/<skill-name>/` in the project root

Get the repository if it isn't already local:

```sh
git clone --depth 1 https://github.com/hemapriyan-rk/claude-rigor-skills.git
```

Copy each chosen skill folder, keeping everything inside it. Some skills include `assets/` or `scripts/` that they need:

```sh
cp -r claude-rigor-skills/skills/<skill-name> ~/.claude/skills/
```

On Windows PowerShell:

```powershell
Copy-Item -Recurse claude-rigor-skills\skills\<skill-name> "$HOME\.claude\skills\"
```

Only copy folders from `skills/`. Don't copy `README.md`, `SKILLS.md`, `INSTALL.md`, or `LICENSE` into the skills directory.

## 6. Verify and finish

1. Check that each installed folder contains a `SKILL.md`.
2. Tell the user which skills were installed and where.
3. Tell them the skills load when a new Claude Code session starts, so they should restart the session.
4. Mention that they can remove a skill later by deleting its folder, or add more by asking again.

Delete the cloned copy if you cloned it into a temporary location.
