"""Dashboard endpoint: top customers by paid revenue in the last N days."""

import sqlite3
import sys
import time

AS_OF = "2026-10-01"


def top_customers(conn, days=30, limit=10):
    since = conn.execute("SELECT date(?, ?)", (AS_OF, f"-{days} days")).fetchone()[0]
    results = []
    for customer_id, name, country in conn.execute("SELECT id, name, country FROM customers"):
        rows = conn.execute(
            "SELECT amount_cents FROM orders "
            "WHERE customer_id = ? AND status = 'paid' AND date(created_at) >= ?",
            (customer_id, since),
        ).fetchall()
        total = sum(r[0] for r in rows)
        if total > 0:
            results.append({"id": customer_id, "name": name, "country": country,
                            "orders": len(rows), "revenue_cents": total})
    results.sort(key=lambda r: (-r["revenue_cents"], r["id"]))
    return results[:limit]


if __name__ == "__main__":
    conn = sqlite3.connect(sys.argv[1] if len(sys.argv) > 1 else "shop.db")
    start = time.perf_counter()
    top = top_customers(conn)
    elapsed = time.perf_counter() - start
    for row in top:
        print(row)
    print(f"took {elapsed:.2f}s")
