"""Create shop.db: 1,000 customers and 50,000 orders over the last year (deterministic)."""

import random
import sqlite3
from datetime import datetime, timedelta

rng = random.Random(42)
conn = sqlite3.connect("shop.db")
conn.executescript("""
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS customers;
CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT NOT NULL, country TEXT NOT NULL);
CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    created_at TEXT NOT NULL,
    amount_cents INTEGER NOT NULL,
    status TEXT NOT NULL
);
""")
countries = ["IN", "US", "DE", "BR", "JP", "GB"]
conn.executemany("INSERT INTO customers VALUES (?, ?, ?)",
                 [(i, f"Customer {i}", rng.choice(countries)) for i in range(1, 1001)])
now = datetime(2026, 10, 1, 12, 0, 0)
rows = []
for i in range(1, 50_001):
    ts = now - timedelta(seconds=rng.randint(0, 365 * 24 * 3600))
    rows.append((i, rng.randint(1, 1000), ts.strftime("%Y-%m-%d %H:%M:%S"),
                 rng.randint(500, 50_000), rng.choice(["paid", "paid", "paid", "refunded", "pending"])))
conn.executemany("INSERT INTO orders VALUES (?, ?, ?, ?, ?)", rows)
conn.commit()
print("seeded", conn.execute("SELECT count(*) FROM orders").fetchone()[0], "orders")
