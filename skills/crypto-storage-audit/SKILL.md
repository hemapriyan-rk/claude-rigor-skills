---
name: crypto-storage-audit
description: Audit code that implements encryption, key management, or secure/policy-gated storage — envelope encryption (DEK/KEK), key derivation, access-policy enforcement, secure deletion. Use for any code handling encryption keys, an encrypted file format, or gated decryption logic. This checks for the specific mistakes that make real-world crypto implementations fail even when the chosen algorithms are correct.
---

# Crypto / Secure Storage Audit

Almost no real-world crypto breaks because the algorithm was weak. It breaks because of key handling, nonce reuse, or a policy check enforced in the wrong layer. This skill checks those specifically, not whether AES is a good cipher.

## Check these, in order of how often they're the actual bug

1. **Hand-rolled primitives** — any custom encryption, hashing, or "obfuscation" scheme that isn't a standard, reviewed algorithm via a maintained library. This is an automatic highest-severity finding regardless of how the rest of the code looks — no amount of surrounding code quality offsets inventing your own crypto.
2. **Nonce/IV reuse** — the single most common real-world implementation bug. Check that every encryption operation uses a nonce/IV that is never reused with the same key, and that the generation mechanism actually guarantees this (a counter that can reset, or randomness with a birthday-bound collision risk at the actual usage volume, both count as reuse risk).
3. **Key hierarchy correctness (DEK/KEK or similar envelope schemes)** — verify the data-encryption key is never written to persistent storage or logs in plaintext, and that only the key-encryption key (itself protected, e.g. by a hardware-backed keystore or policy gate) ever touches the DEK in the clear, and only in memory.
4. **Policy/access-control enforcement point** — for policy-gated decryption, verify the gate is actually enforced at the point of decryption/key release, not just at a UI layer or an earlier check that a different code path can bypass. Trace the actual call path from "user requests access" to "key is released" and confirm the check is on that path, not adjacent to it.
5. **Timing side-channels** — secret comparisons (key checks, MAC verification, password/token checks) using standard `==`/string comparison instead of a constant-time comparison function leak information via timing.
6. **Key rotation / revocation** — confirm that rotating or revoking a key actually invalidates access through the old key, rather than just adding a new key alongside an old one that still works.
7. **Secure deletion** — if the design claims data becomes unrecoverable after key deletion (crypto-shredding), confirm the deleted key is actually the *only* copy — check for cached copies, swap/paging exposure, or a backup path that still holds it.

## Output format

```
## [Finding class]
- Location: [exact file/function]
- What's wrong: [specific, not "could be improved"]
- Why it matters: [the concrete way this fails in practice]
- Fix: [specific]
```

A hand-rolled primitive or a confirmed nonce-reuse pattern goes at the top regardless of anything else found — these are the findings that actually break real systems, and burying them under a long list of minor items defeats the point of the audit.
