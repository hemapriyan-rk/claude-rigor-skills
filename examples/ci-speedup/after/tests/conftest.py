import pytest

from orders.store import create_store, load_reference_data


@pytest.fixture(scope="session")
def _reference_store():
    conn = create_store()
    load_reference_data(conn)
    yield conn
    conn.close()


@pytest.fixture
def store(_reference_store):
    # Reference data is read-only in tests; only orders are written, so clear them after each test.
    yield _reference_store
    _reference_store.execute("DELETE FROM orders")
    _reference_store.commit()
