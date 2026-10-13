"""Token-bucket rate limiter used by the public API gateway."""

import time


class RateLimiter:
    def __init__(self, capacity, refill_per_second, clock=time.monotonic):
        self.capacity = capacity
        self.refill_per_second = refill_per_second
        self.clock = clock
        self.buckets = {}

    def _refill(self, key):
        tokens, last = self.buckets.get(key, (self.capacity, self.clock()))
        now = self.clock()
        tokens = min(self.capacity, tokens + (now - last) * self.refill_per_second)
        self.buckets[key] = (tokens, now)
        return tokens

    def allow(self, key, cost=1):
        """Return True and spend `cost` tokens if `key` has enough, else False."""
        tokens = self._refill(key)
        if tokens >= cost:
            self.buckets[key] = (tokens - cost, self.buckets[key][1])
            return True
        return False

    def retry_after(self, key, cost=1):
        """Seconds until `key` could afford `cost` tokens."""
        tokens = self._refill(key)
        return max(0.0, (cost - tokens) / self.refill_per_second)
