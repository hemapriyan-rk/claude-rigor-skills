# Demo: `performance-optimization` on a slow report script

Run on 2026-10-13 in a fresh, headless Claude Code session (Claude Code 2.1.296, model `claude-sonnet-5-5`) in a folder containing only [`report_before.py`](report_before.py) (as `report.py`) and the skill. [output.md](output.md) is the session's output, unedited.

## Prompt

```text
Use the performance-optimization skill on report.py. It takes about 8 seconds on 12,000 signups and the real nightly batch is 500,000. Make it fast enough for that.
```

**Tools allowed:** Skill, Read, Edit, Write, Glob, Grep, `python`. **Cost:** $0.16, 97 seconds.

## What to look for

- It profiled with `cProfile` before changing anything and found two O(n²) functions.
- It kept the original "first signup wins" behavior, so the output is identical.
- **Checked independently:** `report_before.py` took 7.5 s and [`report_after.py`](report_after.py) took 0.2 s on the same input, with byte-identical output.
- It said plainly that the 500k figure was a single run and that the old and new versions weren't compared at that size.

Model output varies from run to run, so a re-run will be worded differently.
