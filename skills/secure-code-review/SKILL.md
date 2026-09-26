---
name: secure-code-review
description: Review code, a diff, or a PR for real security and correctness bugs — not style nitpicks. Use before merging anything that crosses a trust boundary (service-to-service calls, user input, file/network I/O, auth checks), whenever the user asks for a code review or security review, or before a patent PoC / project component gets treated as production-ready. Prioritizes exploitable findings over cosmetic ones.
---

# Secure Code Review

A review that produces forty style comments and misses the one auth bypass is worse than no review — it burns the reviewee's attention on noise and buries the thing that matters. This skill finds the thing that matters first.

## Read the whole diff/file before judging anything

Don't review line-by-line in isolation — a change that looks fine alone can break an invariant defined elsewhere in the file. Understand what the code is supposed to guarantee before checking whether it does.

## Check these classes explicitly, in priority order

1. **Trust boundaries** — every point where data crosses from a less-trusted zone to a more-trusted one (user input, another service's response, a file read, a sensor reading, a retrieved document). Is it validated *at the boundary*, or does validation happen somewhere downstream where it's easy to skip on a new code path?
2. **Auth/authz** — is every internal service-to-service call actually authenticated, or does the code assume "it's internal, it's fine"? That assumption is the single most common real-world breach vector in distributed systems — internal trust is not a security boundary.
3. **Race conditions / TOCTOU** — check-then-act patterns on shared state, especially across async boundaries or between a permission check and the operation it gates.
4. **Injection** — anywhere a string gets built from untrusted input and then interpreted (SQL, shell, template, deserialization). Check the actual sink, not just whether input "looks sanitized."
5. **Error handling that swallows security-relevant failures** — a caught exception that logs and continues past a failed auth check or failed validation is a silent bypass.
6. **Secrets** — hardcoded keys/tokens, secrets in logs, secrets in error messages returned to a client.
7. **Unsafe defaults** — fail-open instead of fail-closed on any check that matters.

## Output format

```
## Critical
- [location] — [the actual exploit scenario, concretely, not "this could be unsafe"] — fix: [specific change]

## High / Medium / Low
- same format
```

Rank by exploitability, not by how easy the finding was to spot. A theoretical issue with no realistic attacker path goes in Low even if it's technically incorrect; an easy-to-trigger auth gap goes in Critical even if the fix is a one-liner. State plainly if nothing critical was found — don't manufacture severity to look thorough.
