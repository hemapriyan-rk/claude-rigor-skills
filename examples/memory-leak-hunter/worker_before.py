"""Message worker: validates incoming order messages, prices them, and emits audit events."""

import functools
import json
from collections import defaultdict


class EventBus:
    def __init__(self):
        self._handlers = defaultdict(list)

    def subscribe(self, topic, handler):
        self._handlers[topic].append(handler)

    def unsubscribe(self, topic, handler):
        self._handlers[topic].remove(handler)

    def publish(self, topic, event):
        for handler in list(self._handlers[topic]):
            handler(event)


bus = EventBus()


class RequestContext:
    def __init__(self, message):
        self.message_id = message["id"]
        self.raw = json.dumps(message)          # kept for debugging
        self.audit_log = []


@functools.lru_cache(maxsize=512)
def tax_rate(country):
    rates = {"IN": 0.18, "DE": 0.19, "GB": 0.20, "US": 0.0, "JP": 0.10}
    return rates.get(country, 0.15)


def handle_message(message):
    ctx = RequestContext(message)

    def record_audit(event):
        ctx.audit_log.append(event)

    bus.subscribe("audit", record_audit)

    if message["quantity"] <= 0:
        bus.publish("audit", {"id": ctx.message_id, "event": "rejected"})
        return {"id": ctx.message_id, "status": "rejected", "audit_events": len(ctx.audit_log)}

    subtotal = message["quantity"] * message["unit_price"]
    total = round(subtotal * (1 + tax_rate(message["country"])), 2)
    bus.publish("audit", {"id": ctx.message_id, "event": "priced", "total": total})
    return {"id": ctx.message_id, "status": "ok", "total": total, "audit_events": len(ctx.audit_log)}
