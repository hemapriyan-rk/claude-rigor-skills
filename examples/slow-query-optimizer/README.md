# Demo: `slow-query-optimizer` on a slow dashboard query

Run on 2026-10-19 in a fresh, headless Claude Code session (model `claude-sonnet-5-5`, `--setting-sources project,local` so only this skill was installed) in a folder containing only `dashboard.py`, `seed.py`, the seeded `shop.db`, and the skill. [output.md](output.md) is the session's output, unedited.

## Prompt

```text
Use the slow-query-optimizer skill on dashboard.py. The top-customers dashboard endpoint is too slow against our database (shop.db, about 50,000 orders and growing). Make it fast.
```

**Tools allowed:** Skill, Read, Edit, Write, Glob, Grep, `python`. **Cost:** $0.19, 71 seconds.

## Files

- [`seed.py`](seed.py) builds the SQLite database: 1,000 customers and 50,000 orders, deterministic.
- [`dashboard_before.py`](dashboard_before.py) is the code the session was given: one query per customer (N+1) with `date(created_at)` in the filter.
- [`dashboard_after.py`](dashboard_after.py) is what the session wrote: one `JOIN` + `GROUP BY` query, plus an `ensure_index` helper for a covering index.

## What to look for

- It read the plan and named the cause with numbers: 1,000 queries, each scanning all 50,000 orders, and a `date()` call that blocks any index.
- It fixed the query shape first. That alone took the time to about 0.02 s; the index brought it to milliseconds.
- **Checked independently** on a fresh copy of the database: 4.99 s → 17 ms (new query, no index) → 4.3 ms (with the index). Results were identical to the original for the top 10 and the top 1,000, and for 1, 7, 30, 90 and 365-day windows.
- It flagged its own gaps: `ensure_index` isn't called automatically, and it couldn't measure the index size in this SQLite build.

## Run it yourself

```sh
python seed.py
python dashboard_before.py     # baseline
python -c "import sqlite3, dashboard_after as d; c = sqlite3.connect('shop.db'); d.ensure_index(c); c.commit()"
python dashboard_after.py
```

Model output varies from run to run, so a re-run will be worded differently.
