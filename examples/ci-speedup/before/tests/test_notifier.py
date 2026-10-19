import time

from orders.notifier import Notifier


def test_sends_each_order_once():
    sent = []
    n = Notifier(sent.append)
    for oid in (1, 2, 3):
        n.notify(oid)
    time.sleep(2)  # give the background thread time to send
    assert sent == [1, 2, 3]


def test_records_sent_orders():
    n = Notifier(lambda oid: None)
    n.notify(42)
    time.sleep(2)
    assert n.sent == [42]


def test_slow_sender_still_delivers():
    def slow_send(oid):
        time.sleep(0.05)
    n = Notifier(slow_send)
    for oid in range(5):
        n.notify(oid)
    time.sleep(3)
    assert n.sent == list(range(5))
