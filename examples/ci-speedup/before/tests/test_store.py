import pytest

from orders.store import order_total_cents, place_order

def test_order_total_1(store):
    oid = place_order(store, 1, 7, 2)
    price = store.execute("SELECT price_cents FROM products WHERE id = ?", (7,)).fetchone()[0]
    assert order_total_cents(store, oid) == price * 2

def test_order_total_2(store):
    oid = place_order(store, 2, 14, 3)
    price = store.execute("SELECT price_cents FROM products WHERE id = ?", (14,)).fetchone()[0]
    assert order_total_cents(store, oid) == price * 3

def test_order_total_3(store):
    oid = place_order(store, 3, 21, 4)
    price = store.execute("SELECT price_cents FROM products WHERE id = ?", (21,)).fetchone()[0]
    assert order_total_cents(store, oid) == price * 4

def test_order_total_4(store):
    oid = place_order(store, 4, 28, 5)
    price = store.execute("SELECT price_cents FROM products WHERE id = ?", (28,)).fetchone()[0]
    assert order_total_cents(store, oid) == price * 5

def test_order_total_5(store):
    oid = place_order(store, 5, 35, 1)
    price = store.execute("SELECT price_cents FROM products WHERE id = ?", (35,)).fetchone()[0]
    assert order_total_cents(store, oid) == price * 1

def test_order_total_6(store):
    oid = place_order(store, 6, 42, 2)
    price = store.execute("SELECT price_cents FROM products WHERE id = ?", (42,)).fetchone()[0]
    assert order_total_cents(store, oid) == price * 2

def test_order_total_7(store):
    oid = place_order(store, 7, 49, 3)
    price = store.execute("SELECT price_cents FROM products WHERE id = ?", (49,)).fetchone()[0]
    assert order_total_cents(store, oid) == price * 3

def test_order_total_8(store):
    oid = place_order(store, 8, 56, 4)
    price = store.execute("SELECT price_cents FROM products WHERE id = ?", (56,)).fetchone()[0]
    assert order_total_cents(store, oid) == price * 4

def test_order_total_9(store):
    oid = place_order(store, 9, 63, 5)
    price = store.execute("SELECT price_cents FROM products WHERE id = ?", (63,)).fetchone()[0]
    assert order_total_cents(store, oid) == price * 5

def test_order_total_10(store):
    oid = place_order(store, 10, 70, 1)
    price = store.execute("SELECT price_cents FROM products WHERE id = ?", (70,)).fetchone()[0]
    assert order_total_cents(store, oid) == price * 1

def test_order_total_11(store):
    oid = place_order(store, 11, 77, 2)
    price = store.execute("SELECT price_cents FROM products WHERE id = ?", (77,)).fetchone()[0]
    assert order_total_cents(store, oid) == price * 2

def test_order_total_12(store):
    oid = place_order(store, 12, 84, 3)
    price = store.execute("SELECT price_cents FROM products WHERE id = ?", (84,)).fetchone()[0]
    assert order_total_cents(store, oid) == price * 3


def test_rejects_zero_quantity(store):
    with pytest.raises(ValueError):
        place_order(store, 1, 1, 0)


def test_rejects_unknown_product(store):
    with pytest.raises(KeyError):
        place_order(store, 1, 999999, 1)
