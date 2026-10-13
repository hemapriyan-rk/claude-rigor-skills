# Demo: `patent-novelty-evaluator` on a drowsiness-detecting helmet

Run on 2026-10-13 in a fresh, headless Claude Code session (Claude Code 2.1.296, model `claude-sonnet-5-5`) in a folder containing only the prompt and the skill. [output.md](output.md) is the session's output, unedited.

## Prompt

```text
Use the patent-novelty-evaluator skill. Invention: a motorcycle helmet with a dry-electrode EEG band in the liner and an IMU. It flags rider drowsiness only when EEG alpha/theta power rises AND the IMU detects head-nodding within the same 10-second window, then vibrates the helmet and sends an alert to a paired phone. I want to file in India.
```

**Tools allowed:** Skill, Read, WebSearch, WebFetch. **Cost:** $0.65, 183 seconds, about 13 searches and 9 documents.

## What to look for

- Verdict: **Weak (needs rework)**. A 2014 smart-helmet paper read in full discloses most elements; only the hard AND-gating rule wasn't found.
- It applied India's tests (Section 2(1)(ja) inventive step, Section 3(k) exclusions) and gave seven concrete ways to strengthen the claim.
- Its search log says what wasn't checked, including InPASS and CPC-filtered searches.
- It went over the skill's default budget of 6 documents (9 opened). Not legal advice.

Model output varies from run to run, so a re-run will be worded differently.
