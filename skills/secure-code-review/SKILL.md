---
name: secure-code-review
description: Review code, a diff, or a PR for exploitable security and correctness bugs, ranked by real attacker impact, not style. Use for code or security review requests and before merging anything that crosses a trust boundary (user input, auth, service calls, file or network I/O).
---

# Secure Code Review

A review that lists forty style nits and misses the one auth bypass is worse than no review. Find what an attacker can actually use, prove it with a concrete request, and stop.

## 1. Set scope and budget

- **Review what was asked.** For a diff or PR, review the changed lines plus the code they call into. For a file, that file plus the functions it calls. Don't read the whole repository unless asked to.
- **Size the effort to the risk.** Code handling auth, payments, crypto, file paths, or shell/SQL gets the full checklist. Internal utilities with no untrusted input get a quick pass of steps 2 and 3 only.
- **Read everything you need in one step.** Read the code together with the reference files that apply, in parallel. The references are in this skill's base directory: `references/auth-checklist.md` if the code handles login, sessions, tokens, password reset, or role checks; `references/sinks.md` if it builds SQL, shell commands, file paths, templates, or outbound URLs. Skip any reference that doesn't apply.
- **Read the whole unit once before judging lines.** A line that looks fine alone can break an invariant set elsewhere in the file.

## 2. Map trust boundaries

List every place untrusted data enters: request bodies, headers, query strings, cookies, file contents, environment, other services' responses, database values written by users. Then follow each one to where it is used. Most real bugs sit on these paths.

## 3. Check in priority order

1. **Authentication and authorization.** Who is the caller, and how is that proven? Any identity taken from a client-controlled header, any "internal" caller trusted without proof, any check that fails open on an exception. Go through every item in `references/auth-checklist.md` that applies.
2. **Injection.** Untrusted data reaching an interpreter: SQL, shell, templates, deserializers, file paths, URLs fetched server-side. Check the actual sink, not whether input "looks sanitized." Use the section of `references/sinks.md` for the language in front of you.
3. **Races and TOCTOU.** Check-then-act on shared state, especially between a permission check and the action it guards, or a read-then-update of a single-use token.
4. **Swallowed failures.** A caught exception that logs and continues past a failed check is a silent bypass.
5. **Secrets.** Hardcoded keys, secrets in logs or error responses.
6. **Unsafe defaults.** Fail-open behavior, debug modes, permissive CORS, missing rate limits on credential endpoints.

## 4. Prove each finding

For every finding, state the exact input or request that exploits it and what the attacker gets. If you can't construct one, it's Low or not a finding. Don't report theoretical issues as Critical.

Before reporting, check coverage: every checklist item you went through is either a finding or something you confirmed is handled. Minor items still go in Low, in one line each.

## 5. Report

Use this format. Rank by exploitability, not by how easy the finding was to spot.

```
## Critical | High | Medium | Low
- `file:line` **What's wrong.** Exploit: <the request or input> → <what the attacker gets>. Fix: <the specific change>.
```

For example:

```
## Critical
- `routes/files.js:9` **SQL injection in rename.** Exploit: `{"id": "1 OR 1=1", "name": "x"}` → renames every file. Fix: `db.run("UPDATE files SET name = ? WHERE id = ? AND owner_id = ?", name, id, req.user.id)`.
```

- One finding per root cause. Merge duplicates.
- End with one line naming what to fix first.
- If nothing is Critical, say so plainly. Don't pad the list to look thorough.
