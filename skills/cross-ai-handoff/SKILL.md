---
name: cross-ai-handoff
description: Distill a Claude conversation or project into a self-contained, model-agnostic brief for use with a different AI system (ChatGPT, Gemini, Grok, a local LLM, etc.) that has no access to this conversation, Claude's memory, or Claude-specific artifacts. Use whenever the user asks to take this context to another AI, get a second opinion elsewhere, or continue this work in a different tool. Do not use this for handoff to Claude Code — use the `code-handoff` skill for that, since it can assume a shared Claude context this skill cannot.
---

# Cross-AI Handoff

The failure mode this skill prevents: a brief that references "as discussed above," Claude's memory files, or artifact links that mean nothing outside this session — so the receiving model either fabricates the missing context or asks the user to re-explain everything by hand.

## What makes a handoff actually portable

1. **Strip every self-referential pointer.** No "as we discussed," no reference to a memory file, project, or artifact link the other model can't open. Every fact the other model needs has to be restated as plain content, not pointed at.
2. **State the target model's capability envelope if known.** If the receiving model has no web access, don't tell it to "look this up" — include the actual finding instead. If it has a smaller context window, prioritize what's load-bearing over completeness.
3. **Separate fact from inference.** State plainly what was verified (with source) versus what Claude concluded or recommended — the other model needs to know which parts to trust as given and which parts it's free to re-evaluate.
4. **Carry over every caveat explicitly — don't let compression flatten them.** If the original conversation hedged something ("this works for the tested case but hasn't been checked against X"), that hedge has to survive the compression or the other model will present it with false confidence. This is the single most common thing lost in a handoff.

## Output structure

```markdown
# Context for [other model]

## Situation
(what this is, one paragraph, no references to "this conversation")

## Verified facts (with source)
- ...

## Claude's analysis / recommendation (marked as such, not fact)
- ...

## Caveats and unresolved uncertainty — do not present these as settled
- ...

## Constraints / decisions already made
- ...

## The actual ask
(the specific question or task for the receiving model — one clear ask, not a vague "thoughts?")
```

## Anti-pattern

Don't just paste a conversation summary and call it portable — a summary optimized for a human reader who already has the context is not the same as a brief for a model that has none. Every fact has to stand on its own, and every caveat from the original has to survive, otherwise the other model's output will look more confident than the underlying research actually supports.
