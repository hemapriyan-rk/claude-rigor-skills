# Demo: `architecture-design` on a ride-hailing location service

Run on 2026-10-13 in a fresh, headless Claude Code session (Claude Code 2.1.296, model `claude-sonnet-5-5`) in a folder containing only the prompt and the skill. [output.md](output.md) is the session's output, unedited.

## Prompt

```text
Use the architecture-design skill: design the backend for live driver locations in a ride-hailing app. 40,000 active drivers send GPS every 4 seconds, riders must see nearby drivers within 1 second, target 99.9% availability, one cloud region, a team of 4 engineers.
```

**Tools allowed:** Skill, Read. **Cost:** $0.20, 84 seconds.

## What to look for

- It turned the requirements into numbers (10k writes/s, 43.8 min/month error budget) and stated its assumptions.
- It named the trade-offs and what each gives up, including a rejected alternative.
- Its break scenarios surfaced a question the prompt didn't answer: whether dispatch depends on the location store.
- It pointed out that "within 1 second" can only mean pipeline latency, because the 4-second GPS interval sets how fresh the map can be.

Model output varies from run to run, so a re-run will be worded differently.
