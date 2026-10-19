## Result
`top_customers` (30 days, top 10): **6.52 s → about 0.003 s** on 50,000 orders and 1,000 customers. The results are identical. I compared the old and new implementations as full lists, including order, for five `days`/`limit` combinations: (30,10), (7,10), (90,25), (365,1000) and (1,5).

## Cause
The code ran one query per customer (1,000 queries). With no index on `orders`, each query scanned all 50k rows. That is about 50 million row visits per request. `date(created_at) >= ?` also stopped any index on `created_at` from being used.

## Change
- **`dashboard.py:10`:** `top_customers` is now one `JOIN` + `GROUP BY` query, with `ORDER BY revenue DESC, c.id LIMIT ?` done in SQL. The `date()` wrapper is gone. It's equivalent here because `since` is a plain date and `created_at` is `YYYY-MM-DD HH:MM:SS`.
- **New `ensure_index(conn)` in `dashboard.py`:** it creates this index, which I also applied to `shop.db`:
  ```sql
  CREATE INDEX idx_orders_status_created_customer_amount
  ON orders (status, created_at, customer_id, amount_cents);
  ```
  - The plan is now `SEARCH o USING COVERING INDEX ... (status=? AND created_at>?)`, with no table scan and no table lookups.
  - Just removing the N+1 already got it to about 0.02 s. The index takes it to about 0.0025 s and keeps it from growing with the table.
  - `ensure_index` is not called from `__main__` or `top_customers`, so a fresh database needs it run once. I applied it to `shop.db` myself.

## Cost and rollout
- **Index size:** I couldn't measure it because `dbstat` isn't available in this SQLite build. `shop.db` is 12.4 MB in total, and I'd expect the index to add roughly 2 MB.
- **Write cost:** every insert into `orders` now also updates this index, and so does any update to `status`, `created_at`, `customer_id` or `amount_cents`.
- **Rollout:** SQLite's `CREATE INDEX` locks the database while it builds. On 50k rows that takes well under a second. Run it in a quiet window if the table is much bigger in production.

I didn't touch `seed.py`.