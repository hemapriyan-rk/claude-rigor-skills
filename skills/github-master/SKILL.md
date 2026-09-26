---
name: github-master
description: Manage a project's git/GitHub workflow end to end — connecting a local repo to a GitHub remote, disciplined local auto-checkpoint commits during active work, commit message quality, and safe local-to-remote sync (fetch-before-push, branch strategy, no blind force-pushes). Use whenever the user asks to set up git/GitHub for a project, wants work checkpointed or committed automatically during a session, needs help pushing/pulling/syncing with a remote, or is deciding on a branching strategy.
---

# GitHub Master

Local checkpointing and remote publishing are different risk levels wearing the same word, "commit." This skill automates the low-risk one freely and treats the high-risk one — anything that touches a shared or public remote — as something to keep visible and confirmable, not something to run silently just because it's scriptable.

## GitHub connection

- Check for an existing remote first (`git remote -v`) before assuming one needs to be created.
- If a new remote is needed: use the `gh` CLI if it's available and authenticated (`gh auth status`, then `gh repo create`), or ask the user for the repo URL if it's already been created on GitHub's side — never fabricate a repo URL or assume one exists.
- Default to **private** visibility for a newly created repo unless the user says otherwise. Once a repo has been public even briefly, its history can already be cloned or indexed elsewhere — "make it private again later" doesn't fully undo that, so get the default right the first time rather than fixing it after.
- Add the remote (`git remote add origin <url>`) and set upstream on first push (`git push -u origin <branch>`).
- Creating a new remote repo and the first push to it are exactly the kind of action to confirm with the user before executing, especially around visibility — state what's about to happen and wait rather than assuming silent approval.

## Auto-checkpoint discipline

The point of checkpointing is a safety net during active work, not the final shape of the project's history.

- Checkpoint before any risky or large edit (a refactor, a dependency upgrade, a broad generated-code pass) and at natural stopping points, so a bad edit or a crashed session never costs more than a few minutes of work.
- Use `scripts/checkpoint.sh` for this: it stages everything and commits only if there's an actual change, and is a no-op (not an empty commit) on a clean tree. Run it as `scripts/checkpoint.sh "short note"` — the note is optional.
- Checkpoint commits are local-first: don't push every checkpoint to the remote by default — that turns the remote history into noise for anyone else pulling it. Push checkpoints only when the user is working solo on a private branch and has said that's what they want; otherwise, clean up (squash/rebase) checkpoint commits into a coherent history before they reach a shared branch.
- Checkpoint messages carry an obvious `checkpoint:` prefix specifically so they're easy to identify and clean up later — never let a throwaway checkpoint message quietly become part of the permanent, shared history without the user noticing.

## Commit message quality

- A commit message says what changed and why — not a restatement of the diff. If the repo already has a convention (check recent `git log` — conventional-commits prefixes like `feat`/`fix`/`chore`/`refactor`, or something else entirely), follow it rather than inventing a new one.
- One logical change per commit: don't split a single change across several commits, and don't bundle unrelated changes into one "misc fixes" commit — both make the history harder to bisect or revert later, which is the actual point of a commit history existing at all.
- Never commit a secret, credential, or key. Check the staged diff for obvious secret patterns before committing — and if the repo does handle credentials or crypto material, run `secure-code-review` or `crypto-storage-audit` on the change first. A secret removed in a later commit is still in history and has to be treated as compromised and rotated, not just deleted.

## Local ↔ remote sync

- **Fetch before push.** Run `git fetch` and check for divergence before pushing — a rejected push is git protecting against overwriting someone else's history, not a bug to route around. Resolve divergence with a rebase or merge, chosen deliberately (see below), not by forcing past the rejection.
- **Force-push is a last resort, never a default.** Only use `--force`/`--force-with-lease` on a branch known to be exclusively the user's own — never on a shared branch (`main`/`master` or any branch others pull from) without the user's explicit confirmation, since a force-push can permanently discard commits from the remote that others haven't fetched yet. Prefer `--force-with-lease` over bare `--force` when it's genuinely needed — it fails safely if the remote moved since it was last checked, instead of overwriting blind.
- **Branch strategy**: keep in-progress work on short-lived feature branches, merge or PR into the main line rather than committing large in-progress changes directly to a shared branch. This is what actually keeps local experimentation separable from the canonical shared history.
- **When local and remote have diverged** (both have commits the other doesn't), say so plainly before resolving it. The choice between merge and rebase changes the resulting history — that's a decision worth surfacing explicitly, not one to make silently on the user's behalf.

## Anti-patterns

- Committing generated/build artifacts or dependency directories that belong in `.gitignore` instead.
- Running an automated commit without checking `git status`/`git diff` first — an automated commit that includes an unintended file (local config, a debug print, a secret) is worse than no automation at all.
- Treating "commit automatically" as license to also push automatically. Local checkpointing is safe to automate; anything that reaches a shared or public remote stays visible and confirmable, especially the first time in a session.
