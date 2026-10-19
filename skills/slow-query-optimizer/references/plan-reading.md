# Reading query plans

## Getting a real plan

| Database | Command | Notes |
|---|---|---|
| **Postgres** | `EXPLAIN (ANALYZE, BUFFERS, VERBOSE) <query>` | Runs the query. Times are per loop in ms: multiply by `loops` for the node's total |
| **MySQL 8.0.18+** | `EXPLAIN ANALYZE <query>` | Runs the query. Shows `actual time=first..last rows=N loops=N` per iterator |
| **MySQL (older)** | `EXPLAIN FORMAT=JSON <query>` | Estimates only. Pair with slow query log timings |
| **SQLite** | `EXPLAIN QUERY PLAN <query>` | Shows access path only (`SCAN` vs `SEARCH ... USING INDEX`). Time the query separately |

For write statements, run inside `BEGIN; ... ROLLBACK;`.

## Red flags

| Pattern in the plan | What it usually means |
|---|---|
| `Seq Scan` (Postgres), `type: ALL` / `Table scan` (MySQL), `SCAN table` (SQLite) on a large table with a selective `WHERE` | Missing index, or an index the predicate can't use |
| `rows=` estimate off by 10× or more from actual | Stale statistics, correlated columns, or a function/expression in the predicate |
| `Nested Loop` with `loops=` in the thousands | Join order or missing index on the inner side; sometimes an N+1 in disguise |
| `Sort Method: external merge Disk` | Sort spilled to disk: missing index for `ORDER BY`, or `work_mem` too small |
| `Hash ... Batches: >1` | Hash join spilled to disk |
| `Rows Removed by Filter` large compared to rows returned | Index is too broad, or filter not part of the index |
| `Index Scan` followed by many heap fetches | A covering index (`INCLUDE` in Postgres) may remove the lookups |
| `USE TEMP B-TREE FOR ORDER BY` (SQLite), `Using filesort` (MySQL) | Sort not served by an index |
| `Limit` over a large `OFFSET` | Every skipped row is still read: switch to keyset pagination |

## N+1 detection

A single plan can't show N+1. Count queries per request instead:

| Stack | How to count |
|---|---|
| Django | `django.db.connection.queries`, `assertNumQueries`, django-debug-toolbar |
| SQLAlchemy | `echo=True`, or an event listener on `before_cursor_execute` |
| Rails | Log lines per request, the `bullet` gem |
| Prisma | `log: ['query']` |
| Any | Database statement log with request IDs; `pg_stat_statements` call counts |

Many near-identical queries differing only in an ID is the signature.
