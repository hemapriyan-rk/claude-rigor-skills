# Demo: `researcher` on phone-only acoustic indoor localization

Run on 2026-10-13 in a fresh, headless Claude Code session (Claude Code 2.1.296, model `claude-sonnet-5-5`) in a folder containing only the prompt and the skill. [output.md](output.md) is the session's output, unedited.

## Prompt

```text
Use the researcher skill: does anything already exist that does room-level indoor localization using only a phone's own speaker and microphone (ultrasonic chirps), with no installed beacons? Standard depth.
```

**Tools allowed:** Skill, Read, WebSearch, WebFetch. **Cost:** $0.34, 81 seconds, 11 searches and 3 page reads (within the Standard budget).

## What to look for

- It stated what would falsify the claim before searching.
- It killed the claim with a peer-reviewed 2018 paper it read directly, plus a granted patent, and listed the gaps a narrower claim could target.
- It marked which sources were read in full and which were seen only through search summaries, and said its patent coverage was shallow.

Model output varies from run to run, so a re-run will be worded differently.
