# Auth checklist

Open this when the code handles login, sessions, tokens, password reset, or role checks. Check each item that applies; skip the rest.

## Identity

- [ ] The caller's identity comes from a verified credential (signed session, verified JWT, mTLS identity), never from a header, query parameter, or body field the client controls (`X-User-Id`, `user_id` in the body, `role` in a cookie).
- [ ] "Internal" or "service" callers prove who they are (mTLS, signed service token). A header like `X-Internal: true` or a source-IP check behind a proxy is not proof.
- [ ] JWTs: signature verified, `alg` pinned (reject `none` and algorithm switching), `exp` checked, audience and issuer checked.

## Authorization

- [ ] Every protected route checks authorization, including admin, export, delete, and bulk endpoints.
- [ ] Object access checks ownership (`WHERE id = ? AND owner_id = ?`), not just that the user is logged in. Missing ownership checks are IDOR.
- [ ] The check fails **closed**: any exception, missing field, or `None` result denies access.
- [ ] The check and the action use the same data. A permission checked on one ID and an action applied to another is a bypass.

## Passwords

- [ ] Hashed with a slow, salted algorithm: argon2id, bcrypt, or scrypt. MD5, SHA-1, and unsalted SHA-256 are findings.
- [ ] Login has rate limiting or lockout per account and per IP.
- [ ] Error messages don't reveal whether the username exists, if account enumeration matters here.

## Tokens (reset, invite, API, session)

- [ ] Generated with a CSPRNG: `secrets` (Python), `crypto.randomBytes` (Node), `crypto/rand` (Go), `SecureRandom` (Java). `random`, `Math.random`, and timestamps are findings.
- [ ] Long enough to resist guessing: at least 128 bits. A 6-digit code needs strict attempt limits.
- [ ] Expiry is stored **and checked** at use time.
- [ ] Single use: invalidated atomically when used (`UPDATE ... WHERE token = ? AND used = 0`, then check the affected row count).
- [ ] Compared in constant time: `hmac.compare_digest`, `crypto.timingSafeEqual`, `subtle.ConstantTimeCompare`, `MessageDigest.isEqual`.
- [ ] Null and empty cases handled: a missing stored token must not match a missing submitted token (`None == None`, `null === null`, `"" == ""`).
- [ ] Stored hashed where a database leak would let an attacker use them.
- [ ] Never logged, and never returned in responses or error messages.

## Sessions

- [ ] Session ID rotated on login and privilege change.
- [ ] Cookies set `HttpOnly`, `Secure`, and an appropriate `SameSite`.
- [ ] Logout and password change invalidate existing sessions server-side.
- [ ] State-changing requests are protected against CSRF when cookies carry auth.
