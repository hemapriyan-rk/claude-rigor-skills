---
name: code-handoff
description: Package a design/ideation conversation into a self-contained handoff brief for a coding agent (Claude Code or a fresh coding session) so implementation starts from locked decisions instead of re-deriving context or re-exploring already-rejected approaches. Use whenever the user says they're moving from planning/chat into building, asks to "hand this off to Claude Code," or wants a task prompt/context file to paste into a coding session. Do not use this to write the actual implementation — only to produce the handoff artifact.
---

# Code Handoff (Chat → Coding Agent)

The failure mode this skill prevents: Claude Code starts a fresh session with no memory of the design conversation, re-derives requirements from scratch, re-explores an approach that was already ruled out, and quietly makes a decision the user thought was already settled. The fix is a handoff document that contains decisions, not vibes.

## What to extract from the conversation

Pull these out explicitly — don't paraphrase into vaguer language, keep the actual constraints as stated:

1. **Goal** — one line, the actual deliverable.
2. **Decisions already locked** — bullet list of choices already made in this conversation (stack, approach, architecture, format). These are not up for re-litigation by Claude Code.
3. **Explicitly open items** — anything still undecided. Mark these clearly as "needs input" so Claude Code doesn't silently pick an answer and present it as settled.
4. **Dead ends already ruled out, and why** — this is the highest-value section and the one most often skipped. If an approach was considered and rejected, say so and say why, or Claude Code will burn time re-discovering the same dead end.
5. **Environment / stack constraints** — language, framework, existing repo conventions, dependencies that are fixed vs. flexible.
6. **File/repo layout** — if one exists or is expected, state it; if none exists yet, say so explicitly rather than leaving it ambiguous.
7. **Acceptance criteria / definition of done** — testable, not aspirational. "Works well" is not acceptance criteria; "handles input X without exceeding Y ms" is.
8. **Relevant project context** — if this connects to an existing project file/patent/architecture doc the user maintains, name it and summarize only what's load-bearing for this task, not the whole history.

## Output format

A single markdown block, ready to paste as the first message of a Claude Code session (or saved as a context file, e.g. `TASK.md`):

```markdown
# Task: [one-line goal]

## Locked decisions
- ...

## Open — needs input before/while building
- ...

## Ruled out (do not re-explore)
- [approach] — rejected because [reason]

## Environment
- ...

## Definition of done
- ...
```

## Anti-pattern

Don't hand off a vision statement ("build something that detects hazards using multiple cameras"). Hand off the decisions that were actually made in the conversation, the constraints that are actually fixed, and a definition of done that can be checked mechanically. If the conversation didn't actually settle something, mark it "needs input" instead of inventing a plausible-sounding decision to fill the gap — that's exactly the failure mode this skill exists to prevent.
