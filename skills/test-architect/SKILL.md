---
name: test-architect
description: Generate tests focused on edge cases, invalid input, concurrency, and failure injection — not coverage padding. Use whenever the user asks for tests to be written, or when code touches concurrency, external I/O, network calls, or ML inference and needs real confidence rather than a high coverage number. Do not use this to generate ten variations of the same happy-path test.
---

# Test Architect

Ten tests that all exercise the same happy path with different literal values raise the coverage number and raise nothing else. This skill exists to find the tests that would actually have caught a real bug.

## For each function/module, identify

- **Boundary values** — empty, zero, max, one-past-max, negative where unexpected, the specific off-by-one the loop structure invites.
- **Invalid / malformed input** — not just "wrong type" but the malformed-but-plausible input that a real caller would actually send (truncated payload, unexpected encoding, a field that's technically present but empty).
- **Concurrent access patterns** — for anything touching shared state: what happens when two callers hit this at once? Is there a test that actually exercises that, or only single-threaded tests of concurrent-safe-looking code?
- **Failure of each external dependency** — for every network call, DB call, or file I/O: a test for timeout, a test for an error response, a test for a partial/truncated response. "The happy path works" tells you nothing about what happens when the dependency doesn't cooperate, which in a distributed system is most of the time that matters.
- **ML-specific**: out-of-distribution input, adversarial-looking input, and the low-confidence path — does the system's defined fallback (see `ml-security-audit` if one hasn't been checked yet) actually get exercised by a test, or does it only exist in a comment?

## If a real bug from this codebase is known

Prioritize writing the test that would have caught it before writing anything else — a regression test for a bug that already happened is worth more than five speculative edge-case tests.

## Anti-patterns

- Don't inflate the count: report the number of distinct *risks* covered, not the number of test functions written — five tests covering five real risks beats fifteen tests covering three.
- Don't write a test that mirrors the implementation's own logic back at it (asserting the function does what its code says it does, rather than what the spec/contract requires) — that passes even when the implementation itself is wrong.
- Don't skip the concurrency and failure-injection cases because they're harder to set up — those are exactly the cases most likely to be undertested elsewhere, which is why they matter more here.

## Output

For each test added, state which specific risk it covers, in one line — if a test doesn't map to a stated risk, reconsider whether it's earning its place in the suite.
