# Demo: `test-architect` on a token-bucket rate limiter

Run on 2026-10-13 in a fresh, headless Claude Code session (Claude Code 2.1.296, model `claude-sonnet-5-5`) in a folder containing only [`rate_limiter.py`](rate_limiter.py) and the skill. [output.md](output.md) is the session's output, unedited.

## Prompt

```text
Use the test-architect skill to write tests for rate_limiter.py. It guards our public API gateway.
```

**Tools allowed:** Skill, Read, Write, Edit, Glob, Grep, `python`. **Cost:** $0.16, 48 seconds.

## What to look for

- It wrote [`test_rate_limiter.py`](test_rate_limiter.py): 15 tests, each named after the risk it covers.
- 4 tests fail on purpose. Each exposes a real bug in `rate_limiter.py`: a race that lets 50 concurrent calls through a 10-token bucket, a lockout when the clock steps backwards, a misleading `retry_after` for unaffordable costs, and a crash on a zero refill rate.
- **Checked independently:** `python -m pytest -q test_rate_limiter.py` gives 4 failed, 11 passed. `rate_limiter.py` wasn't modified.
- It listed what it deliberately didn't cover, such as unbounded key growth.

Model output varies from run to run, so a re-run will be worded differently.
