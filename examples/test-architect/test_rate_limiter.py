import threading
import time
from concurrent.futures import ThreadPoolExecutor

import pytest

from rate_limiter import RateLimiter


class FakeClock:
    def __init__(self, t=1000.0):
        self.t = t

    def __call__(self):
        return self.t

    def advance(self, dt):
        self.t += dt


@pytest.fixture
def clock():
    return FakeClock()


@pytest.fixture
def limiter(clock):
    return RateLimiter(capacity=5, refill_per_second=1, clock=clock)


def test_new_key_gets_full_burst_then_is_denied(limiter):
    assert [limiter.allow("a") for _ in range(6)] == [True] * 5 + [False]


def test_keys_are_isolated(limiter):
    for _ in range(5):
        limiter.allow("a")
    assert limiter.allow("a") is False
    assert limiter.allow("b") is True


def test_refill_restores_exactly_elapsed_tokens(limiter, clock):
    for _ in range(5):
        limiter.allow("a")
    clock.advance(2)
    assert limiter.allow("a") and limiter.allow("a")
    assert limiter.allow("a") is False


def test_refill_never_exceeds_capacity(limiter, clock):
    limiter.allow("a")
    clock.advance(10_000)
    assert [limiter.allow("a") for _ in range(6)] == [True] * 5 + [False]


def test_fractional_refill_boundary(limiter, clock):
    for _ in range(5):
        limiter.allow("a")
    clock.advance(0.999)
    assert limiter.allow("a") is False
    clock.advance(0.001)
    assert limiter.allow("a") is True


def test_cost_exceeding_remaining_is_denied_and_does_not_spend(limiter):
    assert limiter.allow("a", cost=6) is False
    assert limiter.allow("a", cost=5) is True


def test_cost_equal_to_capacity_allowed_once(limiter):
    assert limiter.allow("a", cost=5) is True
    assert limiter.allow("a", cost=1) is False


def test_negative_cost_cannot_mint_tokens_beyond_capacity(limiter):
    # A negative cost must be rejected or ignored; it must never let a caller
    # exceed the configured burst.
    try:
        limiter.allow("a", cost=-100)
    except ValueError:
        return
    allowed = sum(limiter.allow("a") for _ in range(200))
    assert allowed <= 5


def test_clock_going_backwards_does_not_lock_out_key(limiter, clock):
    limiter.allow("a")
    clock.advance(-3600)  # NTP step / bad clock source
    limiter.allow("a")
    clock.advance(5)  # a few real seconds later, bucket has refilled to capacity
    assert limiter.allow("a") is True


def test_retry_after_new_key_is_zero(limiter):
    assert limiter.retry_after("a") == 0.0


def test_retry_after_is_accurate_and_allow_succeeds_after_waiting(limiter, clock):
    for _ in range(5):
        limiter.allow("a")
    wait = limiter.retry_after("a", cost=2)
    assert wait == pytest.approx(2.0)
    clock.advance(wait)
    assert limiter.allow("a", cost=2) is True


def test_retry_after_does_not_consume_tokens(limiter):
    for _ in range(10):
        limiter.retry_after("a")
    assert limiter.allow("a", cost=5) is True


def test_retry_after_for_unaffordable_cost_is_not_a_misleading_finite_wait(limiter):
    # cost > capacity can never succeed; telling the client "retry in 1s"
    # makes it loop forever. Expect an error or infinity.
    try:
        wait = limiter.retry_after("a", cost=6)
    except ValueError:
        return
    assert wait == float("inf")


def test_zero_refill_rate_retry_after_does_not_crash_gateway(clock):
    lim = RateLimiter(capacity=1, refill_per_second=0, clock=clock)
    lim.allow("a")
    try:
        wait = lim.retry_after("a")
    except ValueError:
        return
    assert wait == float("inf")


def test_concurrent_callers_cannot_overspend_bucket():
    # Clock sleeps to widen the check-then-spend window deterministically.
    def slow_clock():
        time.sleep(0.001)
        return 1000.0

    lim = RateLimiter(capacity=10, refill_per_second=1, clock=slow_clock)
    n = 50
    barrier = threading.Barrier(n)

    def call(_):
        barrier.wait()
        return lim.allow("a")

    with ThreadPoolExecutor(n) as ex:
        results = list(ex.map(call, range(n)))
    assert sum(results) <= 10
