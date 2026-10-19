import pytest

from orders.store import create_store, load_reference_data


@pytest.fixture
def store():
    conn = create_store()
    load_reference_data(conn)
    yield conn
    conn.close()
