# Demo: `secure-code-review` on a planted-bug auth module

This demo is set up so you can check the result yourself:

1. **[auth.py](auth.py)** is a small Flask auth module with eight security flaws written in on purpose. Don't use it for anything real.
2. **[PLANTED.md](PLANTED.md)** is the answer key, written before the review ran.
3. **[review.md](review.md)** is the output of a fresh Claude Code session that had only `auth.py` and the skill, word for word. It never saw the answer key.

## Scorecard

| # | Planted flaw | Result |
|---|---|---|
| 1 | SQL injection in `/login` | ✅ Critical, with a working payload (`admin' --`) |
| 2 | Unsalted MD5 password hashing | ✅ High |
| 3 | Predictable, brute-forceable reset token | ✅ High, tied to the missing rate limit |
| 4 | Reset token expiry never checked | ✅ High |
| 5 | Non-constant-time token comparison | ⚠️ Partial: `hmac.compare_digest` appears in a fix, but not as its own finding |
| 6 | Spoofable `X-Internal-Service` bypass | ✅ Critical |
| 7 | Authorization fails open on exception | ✅ Critical, with the exact request that deletes a user |
| 8 | Caller identity taken from `X-User-Id` | ✅ Critical |

**7 found and 1 partial out of 8 planted.** The review ranked findings by how exploitable they are and put the unauthenticated attack paths first.

### It also found a bug that wasn't planted

> **Password reset takeover with `"token": null`.** For any user who hasn't requested a reset, `reset_token` is `NULL`, which comes back as `None`. Posting `{"email": "victim@x.com", "token": null, "new_password": "..."}` gives `None != None`, which is `False`. The invalid-token check is skipped and the password is overwritten.

This is a real critical bug that the author of the demo didn't intend to plant. Other findings not in the answer key include the reset token being printed to logs, a race between two reset confirmations, and missing login rate limiting.

## Run it yourself

```sh
mkdir demo && cd demo
cp path/to/claude-rigor-skills/examples/secure-code-review/auth.py .
mkdir -p .claude/skills && cp -r path/to/claude-rigor-skills/skills/secure-code-review .claude/skills/
claude -p "Use the secure-code-review skill to review auth.py." --allowedTools "Read,Glob,Grep,Skill"
```

Model output varies from run to run, so your findings may be worded or ordered differently.
