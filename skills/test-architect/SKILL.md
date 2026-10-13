---
name: test-architect
description: Write tests that catch real bugs, not coverage padding. Targets boundaries, malformed input, concurrency, and dependency failures, with each test tied to a named risk. Use when asked to write tests, or for code that touches I/O, network calls, shared state, or ML inference.
---

# Test Architect

Ten tests that run the same happy path with different values raise the coverage number and nothing else. Find the tests that would have caught a real bug, write those, and run them.

## 1. Set scope and budget

- **Test what was asked.** The named function, module, or diff. Don't write tests for the whole codebase unless asked to.
- **Follow the project's conventions.** Use the existing test framework, file layout, fixtures, and mocking style. Look at one existing test file first. If there are no tests yet, use the language's standard choice and say which.
- **Load the risk catalog with the code.** Read `references/risk-catalog.md` from this skill's base directory in the same step as the code under test. It lists failure cases by dependency type so you don't have to recall them.
- **Aim for the fewest tests that cover the most distinct risks.** Five tests covering five risks beat fifteen covering three.

## 2. List the risks before writing tests

For the code under test, list each risk in one line. Check:

- **Boundaries:** empty, zero, one, max, one past max, negative, and the off-by-one the loop invites.
- **Malformed but plausible input:** truncated payloads, wrong encoding, a field present but empty, `null` where an object is expected.
- **Each external dependency failing:** timeout, error response, partial or malformed response. Use the catalog for the dependency type.
- **Concurrency:** for shared state, two callers at once. A single-threaded test of "thread-safe" code proves nothing.
- **ML paths:** out-of-distribution input, and the low-confidence fallback actually being taken.
- **Known bugs:** if a past bug is known, its regression test comes first.

Drop risks that don't apply. Rank the rest by how likely and how costly the failure is.

## 3. Write the tests

- Assert on the **contract** (what the function should do), not on its implementation. A test that mirrors the code passes even when the code is wrong.
- Name each test after the risk it covers: `test_refund_rejects_negative_amount`, not `test_refund_3`.
- Make failure-injection tests deterministic: fake clocks, stubbed dependencies, seeded randomness. A flaky test is worse than none.
- Use property-based tests (Hypothesis, fast-check, `testing/quick`) where a whole input range matters more than a few examples.

## 4. Run them

Run the new tests if the environment allows it. If one fails, decide whether it found a real bug or the test is wrong, and say which. Don't silently change the test to make it pass. If you can't run tests here, give the exact command.

## Output

```
## Risks covered
| Risk | Test | Result |
|---|---|---|
| <one-line risk> | `<test name>` | pass / FAIL: real bug / not run |

## Tests
<the test code>

## Bugs found
<any failing test that exposed a real bug, with the input that triggers it>

## Not covered
<risks deliberately left out, and why>
```
