# Answer key: flaws planted in `auth.py`

These were written into `auth.py` on purpose, before the review ran. The reviewing session never saw this file.

| # | Flaw | Where | Why it's exploitable |
|---|---|---|---|
| 1 | SQL injection | `login()` builds the query with an f-string | A username like `admin' --` skips the password check entirely. |
| 2 | Unsalted MD5 password hashing | `hash_password()` | A leaked database can be cracked quickly with precomputed tables or a GPU. |
| 3 | Predictable, brute-forceable reset token | `request_reset()` uses `random.randint` for a 6-digit code | `random` is not a CSPRNG, and one million possibilities can be guessed with no rate limit. |
| 4 | Reset token expiry never checked | `confirm_reset()` reads `reset_expires` but ignores it | A token stays valid forever until it's used. |
| 5 | Non-constant-time token comparison | `confirm_reset()` compares with `!=` | A timing side channel leaks information about the token. |
| 6 | Spoofable "internal service" bypass | `is_admin()` trusts the `X-Internal-Service` header | Any client can send `X-Internal-Service: billing` and gets admin. |
| 7 | Fail-open authorization | `is_admin()` returns `True` on any exception | A missing or non-numeric `X-User-Id` header grants admin. |
| 8 | Identity taken from a client header | `is_admin()` trusts `X-User-Id` as the caller's identity | Any client can claim to be any user, including an admin. |
