---
name: slow-query-optimizer
description: Speed up slow SQL queries and ORM code with evidence. Reads the real query plan, fixes the actual cause (N+1, missing index, non-sargable filter, bad pagination), and proves it with the same timing before and after, plus a check that results are unchanged. Postgres, MySQL, SQLite.
---

# Slow Query Optimizer

Adding an index because a query "looks slow" is a guess, and guessed indexes slow down every write for nothing. Read the plan, fix what it shows, re-measure the same way, and confirm the query still returns the same rows.

## 1. Set scope and budget

- **Fix what's slow, not everything.** Start from the slow endpoint, job, or query you were given. Don't audit the whole schema.
- **Agree on the target:** which query or endpoint, on what data size, and what time counts as done.
- **Read the references with the code.** In the same step as the query, schema, and ORM code, read `references/plan-reading.md` and `references/fix-catalog.md` from this skill's base directory.
- **Stop when the target is met.** Extra indexes cost writes and storage forever.

## 2. Measure on realistic data

- Run the query plan with real execution, not just an estimate:
  - Postgres: `EXPLAIN (ANALYZE, BUFFERS) <query>`
  - MySQL 8: `EXPLAIN ANALYZE <query>`
  - SQLite: `EXPLAIN QUERY PLAN <query>`, plus wall-clock timing
- `EXPLAIN ANALYZE` actually runs the query. For `INSERT`, `UPDATE` or `DELETE`, wrap it in a transaction and roll back.
- Use production-like row counts. A 1,000-row table hides a sequential scan that 10 million rows exposes.
- For ORM code, count the queries per request (query log, `django.db.connection.queries`, SQLAlchemy echo, Rails log). Many similar queries means N+1, which no single plan will show.
- If you can't reach the database, give the user the exact commands, and work from what they paste. Don't present a guess as a measurement.

## 3. Find the cause in the plan

Look for, in this order:

1. **The node with the most actual time** (Postgres/MySQL), or the full scan on the biggest table (SQLite).
2. **Estimated rows far from actual rows** (10× or more): stale statistics or a predicate the planner can't estimate.
3. **A sequential or full scan with a selective filter:** a missing or unusable index.
4. **Nested loops with thousands of iterations,** sorts or hashes that spill to disk, and `OFFSET` pagination over large row counts.
5. **N+1 query patterns** from the query count.

State the cause in one line, with the plan numbers that show it.

## 4. Fix in order of leverage

1. **Query shape:** collapse N+1 into one query or a batched `IN (...)`; make filters sargable (no function on the indexed column, no leading `%` wildcard, no implicit type casts); replace large `OFFSET` with keyset pagination; select only the columns needed.
2. **Index:** one that matches the actual predicate. Equality columns first, then the range column, then the sort column. Consider a covering or partial index when the plan shows heap lookups or a small hot subset.
3. **Statistics:** `ANALYZE` the table when estimates are far off.
4. **Configuration** (memory settings, planner flags): last, and only with plan evidence.

## 5. Verify

- **Same measurement:** re-run the exact plan and timing from step 2, on the same data.
- **Same results:** compare the old and new query output. Use an order-independent comparison: `EXCEPT` both ways, or sorted row lists or checksums. A faster query with different rows is a regression.
- **Write cost of new indexes:** report the index size and that it adds work to every insert and update on that table.
- **Safe rollout:** create indexes without locking the table where the database supports it (`CREATE INDEX CONCURRENTLY` on Postgres, online DDL on MySQL).

## Output

```
## Result
<query/endpoint>: <before> → <after> on <data size>. Results identical: <how checked>.

## Cause
<one line>, with the plan evidence (node, actual time, rows, loops).

## Change
<the SQL or ORM change and any index DDL>, and why this fix over the alternatives.

## Cost and rollout
<index size, write overhead, how to deploy without locking>.
```

For example: *"`/orders?page=500`: 2.3 s → 0.04 s on 1M rows. `OFFSET 24950` read and discarded 24,950 rows per page; switched to keyset pagination on `(created_at, id)` with a matching index. Results identical: same 50 rows in the same order for pages 1, 250 and 500."*
