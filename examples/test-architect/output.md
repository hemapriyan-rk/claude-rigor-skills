I wrote 15 pytest tests in `test_rate_limiter.py`. Four fail, and I believe all four are real bugs in `rate_limiter.py`. There were no existing tests, so I used pytest with a fake clock to keep them deterministic. The last run was 4 failed, 11 passed.

## Risks covered
| Risk | Test | Result |
|---|---|---|
| New key gets a full burst, then is denied | `test_new_key_gets_full_burst_then_is_denied` | pass |
| One client's usage leaks into another's | `test_keys_are_isolated` | pass |
| Refill is wrong | `test_refill_restores_exactly_elapsed_tokens` | pass |
| Refill overshoots capacity | `test_refill_never_exceeds_capacity` | pass |
| Off-by-epsilon at the refill boundary | `test_fractional_refill_boundary` | pass |
| A denied request still spends tokens | `test_cost_exceeding_remaining_is_denied_and_does_not_spend` | pass |
| Cost equal to capacity | `test_cost_equal_to_capacity_allowed_once` | pass |
| Negative cost mints extra tokens | `test_negative_cost_cannot_mint_tokens_beyond_capacity` | pass |
| Clock steps backwards and locks the key out | `test_clock_going_backwards_does_not_lock_out_key` | **FAIL: real bug** |
| Clock steps backwards and drains tokens | `test_clock_going_backwards_does_not_drain_tokens` | pass |
| `retry_after` on a new key | `test_retry_after_new_key_is_zero` | pass |
| `retry_after` accuracy | `test_retry_after_is_accurate_and_allow_succeeds_after_waiting` | pass |
| `retry_after` consumes tokens | `test_retry_after_does_not_consume_tokens` | pass |
| `retry_after` for a cost that can never succeed | `test_retry_after_for_unaffordable_cost_is_not_a_misleading_finite_wait` | **FAIL: real bug** |
| Zero refill rate | `test_zero_refill_rate_retry_after_does_not_crash_gateway` | **FAIL: real bug** |
| Concurrent callers overspend the bucket | `test_concurrent_callers_cannot_overspend_bucket` | **FAIL: real bug** |

## Bugs found
1. **Concurrency (most serious):** `allow()` checks the balance and then spends it without a lock. With 50 threads released together on a capacity-10 bucket, all 50 were allowed. In production, a burst from one client can get through the limiter. The test widens the race window with a sleeping clock, so it is deterministic. The fix is a `threading.Lock` around the refill, check and spend (or one lock per key).
2. **Clock going backwards:** `_refill` doesn't guard against a negative elapsed time, so tokens go negative and the key is locked out for as long as the step. For example, a 3600 s step back with only 5 s of real time passing leaves that key denied. Use `max(0, now - last)`.
3. **`retry_after` with cost above capacity:** `allow(key, cost=6)` on a capacity-5 bucket can never succeed, but `retry_after` returns `1.0`. A well-behaved client would retry forever. It should raise an error or return infinity.
4. **`retry_after` with `refill_per_second=0`:** it raises `ZeroDivisionError`, which would be a 500 from the gateway. Validate the rate in `__init__` or return infinity.

The negative-cost test passes, but only because the next refill clamps the balance to capacity. `allow(key, cost=-100)` still returns True and spends nothing, so I'd reject negative costs explicitly.

## Not covered
- **Memory growth:** `buckets` never evicts keys, so a flood of unique keys (spoofed IPs) grows it without bound. That needs a design decision on eviction before I can test it.
- **NaN or infinite constructor arguments:** they are unlikely from config, and the other fixes would cover them.
- **Gateway integration:** how the gateway builds the key (for example `X-Forwarded-For` trust) is outside this file.

Run the tests with `python -m pytest -q test_rate_limiter.py` from the `tests2` directory. I didn't change `rate_limiter.py`. I can patch the four bugs if you want.