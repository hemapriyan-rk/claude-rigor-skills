# Fix catalog

## N+1 queries

| Stack | Fix |
|---|---|
| Django | `select_related` (foreign key, one-to-one), `prefetch_related` (many) |
| SQLAlchemy | `selectinload`, `joinedload`, or one query with a `JOIN` and `GROUP BY` |
| Rails | `includes`, `preload`, `eager_load` |
| Prisma | `include`, or one `findMany` with `where: { id: { in: ids } }` |
| Raw SQL | One `JOIN` + `GROUP BY`, or one batched `WHERE id IN (...)` |

## Non-sargable predicates (the index can't be used)

| Slow | Fast |
|---|---|
| `WHERE date(created_at) >= '2026-01-01'` | `WHERE created_at >= '2026-01-01'` |
| `WHERE lower(email) = ?` | Store normalized, or an expression index on `lower(email)` |
| `WHERE name LIKE '%smith'` | Trigram index (Postgres `pg_trgm`) or full-text search |
| `WHERE int_col = '42'` (implicit cast) | Match the column type in the parameter |
| `WHERE a = ? OR b = ?` | `UNION ALL` of two indexed queries, or separate indexes the planner can combine |
| `WHERE col + 1 > ?` | `WHERE col > ? - 1` |

## Index design

- **Column order:** equality columns first, then one range column, then the `ORDER BY` column.
- **Composite beats several single-column indexes** for a combined predicate.
- **Covering index:** add the selected columns (`INCLUDE` in Postgres, trailing columns elsewhere) to avoid table lookups.
- **Partial index:** `WHERE status = 'open'` when queries only touch a small hot subset.
- **Foreign keys:** index the referencing column. Postgres doesn't do it automatically.
- **Every index costs writes and storage.** Drop indexes no query uses (`pg_stat_user_indexes.idx_scan = 0`).

## Pagination

| Slow | Fast |
|---|---|
| `ORDER BY id LIMIT 50 OFFSET 100000` | `WHERE id > :last_seen_id ORDER BY id LIMIT 50` (keyset) |
| `SELECT count(*)` on every page | Cache the count, show an estimate, or drop it |

## Safe index creation

| Database | Command |
|---|---|
| Postgres | `CREATE INDEX CONCURRENTLY ...` (not inside a transaction; check for `INVALID` indexes after a failure) |
| MySQL 8 | `ALTER TABLE ... ADD INDEX ..., ALGORITHM=INPLACE, LOCK=NONE` |
| SQLite | `CREATE INDEX` locks the database while it builds; run it during a quiet window |

## Checking results are unchanged

- `(old_query EXCEPT new_query)` and `(new_query EXCEPT old_query)` both empty (Postgres, SQLite; MySQL 8.0.31+). Use `EXCEPT ALL` when duplicate rows matter.
- Or fetch both result sets, sort, and compare in code.
- Watch for `NULL` handling, duplicate rows, and ordering changes when the original had no `ORDER BY`.
