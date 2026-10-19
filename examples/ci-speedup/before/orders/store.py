"""SQLite-backed order store."""

import sqlite3

SCHEMA = [
    "CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT, country TEXT)",
    "CREATE TABLE products (id INTEGER PRIMARY KEY, sku TEXT, price_cents INTEGER)",
    "CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER, product_id INTEGER, qty INTEGER, status TEXT)",
]


def create_store(path=":memory:"):
    conn = sqlite3.connect(path)
    for stmt in SCHEMA:
        conn.execute(stmt)
    return conn


def load_reference_data(conn):
    """Load the product catalogue and customer list used by every environment."""
    conn.executemany("INSERT INTO products VALUES (?, ?, ?)",
                     [(i, f"SKU-{i:05d}", 100 + (i * 37) % 9900) for i in range(1, 20001)])
    conn.executemany("INSERT INTO customers VALUES (?, ?, ?)",
                     [(i, f"Customer {i}", ["IN", "US", "DE"][i % 3]) for i in range(1, 20001)])
    conn.commit()


def place_order(conn, customer_id, product_id, qty):
    if qty <= 0:
        raise ValueError("qty must be positive")
    if conn.execute("SELECT 1 FROM products WHERE id = ?", (product_id,)).fetchone() is None:
        raise KeyError(product_id)
    cur = conn.execute("INSERT INTO orders (customer_id, product_id, qty, status) VALUES (?, ?, ?, 'new')",
                       (customer_id, product_id, qty))
    conn.commit()
    return cur.lastrowid


def order_total_cents(conn, order_id):
    row = conn.execute("SELECT o.qty * p.price_cents FROM orders o JOIN products p ON p.id = o.product_id "
                       "WHERE o.id = ?", (order_id,)).fetchone()
    return row[0] if row else None
