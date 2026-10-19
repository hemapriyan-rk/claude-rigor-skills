"""Sends order confirmations from a background thread."""

import queue
import threading


class Notifier:
    def __init__(self, send):
        self._send = send
        self._queue = queue.Queue()
        self.sent = []
        threading.Thread(target=self._run, daemon=True).start()

    def notify(self, order_id):
        self._queue.put(order_id)

    def _run(self):
        while True:
            order_id = self._queue.get()
            self._send(order_id)
            self.sent.append(order_id)
            self._queue.task_done()

    def flush(self, timeout=5):
        self._queue.join()
