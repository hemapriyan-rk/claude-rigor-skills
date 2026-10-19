"""Dashboard endpoint: top customers by paid revenue in the last N days."""

import sqlite3
import sys
import time

AS_OF = "2026-10-01"


def top_customers(conn, days=30, limit=10):
    since = conn.execute("SELECT date(?, ?)", (AS_OF, f"-{days} days")).fetchone()[0]
    # One aggregate query; the bare created_at range is sargable and served by
    # idx_orders_status_created_customer_amount (see ensure_index).
    rows = conn.execute(
        "SELECT c.id, c.name, c.country, count(*), sum(o.amount_cents) AS revenue "
        "FROM orders o JOIN customers c ON c.id = o.customer_id "
        "WHERE o.status = 'paid' AND o.created_at >= ? "
        "GROUP BY c.id HAVING revenue > 0 "
        "ORDER BY revenue DESC, c.id LIMIT ?",
        (since, limit),
    ).fetchall()
    return [{"id": i, "name": n, "country": co, "orders": cnt, "revenue_cents": rev}
            for i, n, co, cnt, rev in rows]


def ensure_index(conn):
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_orders_status_created_customer_amount "
        "ON orders (status, created_at, customer_id, amount_cents)"
    )


if __name__ == "__main__":
    conn = sqlite3.connect(sys.argv[1] if len(sys.argv) > 1 else "shop.db")
    start = time.perf_counter()
    top = top_customers(conn)
    elapsed = time.perf_counter() - start
    for row in top:
        print(row)
    print(f"took {elapsed:.2f}s")
