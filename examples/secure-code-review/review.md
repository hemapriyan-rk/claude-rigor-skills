# Review output

Produced on 2026-09-26 by a fresh, headless Claude Code session (Claude Code 2.1.283, model `claude-sonnet-5`) in a folder containing only `auth.py` and the `secure-code-review` skill. The session could read files but not edit them, and never saw [PLANTED.md](PLANTED.md).

```sh
claude -p "Use the secure-code-review skill to review auth.py." --allowedTools "Read,Glob,Grep,Skill"
```

Everything below the line is the session's output, unedited.

---

## Critical

- **`auth.py:70-79` `is_admin` fails open.** The `except Exception` branch logs "allowing request" and returns `True`. `DELETE /admin/users/1` with no headers raises `KeyError` on `X-User-Id`, so the check passes and the user is deleted. The same happens with a non-integer id or an id that isn't in the table, where `fetchone()` returns `None` and `[0]` raises. Fix: return `False` on any exception, or narrow the `except` and deny by default.

- **`auth.py:71-72` and `74` are client-controlled identity headers.** Anyone can send `X-Internal-Service: billing` and get admin. Anyone can also send `X-User-Id: <admin's id>`. Nothing verifies who is calling. The login route returns no session or token, so there is nothing to check these headers against. Fix: issue a signed session or JWT at login and derive the user from that. For billing, use mTLS or a signed service token, and don't trust a plain header.

- **`auth.py:28-31` SQL injection in `/login`.** The username is put into an f-string. `{"username": "admin' --", "password": "x"}` drops the password check and logs in as admin. The same sink allows `UNION`-based extraction of the whole `users` table. Fix: `execute("SELECT id, role FROM users WHERE username = ? AND password_hash = ?", (username, ...))`.

- **`auth.py:60` password reset takeover with `"token": null`.** For any user who hasn't requested a reset, `reset_token` is `NULL`, which comes back as `None`. Posting `{"email": "victim@x.com", "token": null, "new_password": "..."}` gives `None != None`, which is `False`. The invalid-token check is skipped and the password is overwritten. This works against every account that has no reset in flight. Fix: reject the request if the stored token is `None` or the submitted token isn't a non-empty string, and compare with `hmac.compare_digest`.

## High

- **`auth.py:60-61` reset expiry is never enforced.** `reset_expires` is stored and never read in `confirm_reset`, so tokens are valid forever. Fix: require `row[1] and row[1] > time.time()`.

- **`auth.py:40` weak reset token with no attempt limit.** `random.randint(100000, 999999)` uses a non-cryptographic PRNG and gives only 900k values. Combined with no rate limiting on `/password-reset/confirm`, and with expiry not enforced, it can be brute-forced within minutes. Fix: use `secrets.token_urlsafe(32)`, store only a hash of it, add per-account and per-IP rate limits, and invalidate the token after a few failures.

- **`auth.py:20-21` unsalted MD5 password hashing.** A leaked `users.db`, or the injection above, lets an attacker crack most passwords with rainbow tables in seconds. Fix: use `argon2-cffi`, `bcrypt` or `hashlib.scrypt` with a per-user salt, and migrate hashes on next login.

- **`/login` has no rate limiting or lockout.** Combined with fast MD5 and no MFA, credential stuffing is unrestricted. Fix: add throttling per username and per IP.

## Medium

- **`auth.py:93` the reset token is printed to stdout.** Anyone who can read logs can reset any account. It is a placeholder mailer, but it should not ship. Fix: log only that a mail was sent.

- **Concurrent reset confirms.** `confirm_reset` reads the token, then updates it in a separate statement. Two parallel requests with the same token can both succeed. Fix: use a single `UPDATE ... WHERE email = ? AND reset_token = ? AND reset_expires > ?` and check `rowcount`.

- **`auth.py:40-47` reset requests overwrite the token.** An attacker can spam `/password-reset/request` for a victim and keep invalidating the real token, which is a low-effort denial of service. The endpoint also sends a mail whether or not the email exists. Fix: rate-limit it, and don't overwrite a token that is still valid.

## Low

- **Missing keys and wrong types.** `request.json["..."]` raises `KeyError` on a missing key and a `TypeError` on a non-object body, which returns 500 instead of 400. Validate types at the boundary.
- **Connections are never closed.** Every call opens a new `sqlite3` connection and none are closed, which leaks file handles under load.
- **`delete_user` has no guards.** It allows deleting yourself or the last admin.

Most of this is reachable by an unauthenticated attacker, so I'd fix the first four Critical items before anything else. The `is_admin` fail-open, the `null`-token bypass and the injection are each a one-line change. I haven't edited the file. I can apply the fixes if you want.
