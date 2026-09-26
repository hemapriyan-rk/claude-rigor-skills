---
name: ml-security-audit
description: Audit code for adversarial-ML and model-security risk — evasion, data poisoning, model/IP extraction, prompt injection in LLM-agent code, and sensor spoofing in fusion pipelines. Use for any inference pipeline, training loop, LLM agent with tool access, or sensor-fusion/vision code, especially before treating it as production-ready. This is distinct from general security review — it targets attack classes specific to ML systems.
---

# ML Security Audit

General code review checks whether the code does what it's supposed to. This checks whether the *model* can be steered, stolen, or fed false confidence by an attacker who never touches the codebase at all — the attack surface is the data, not just the code.

## Map the attack surface first

Before checking anything, find every point where data an attacker could influence reaches a model: a sensor reading, a user upload, an API request body, a retrieved document, another agent's tool output feeding an LLM's context. Each of these is a separate surface to check below.

## Check each relevant attack class

1. **Evasion** — is there any input validation or sanity bound before inference, or does raw input go straight to the model? Is there confidence thresholding, and does the code have a *defined fallback* for low-confidence or out-of-distribution predictions — or does it silently trust whatever the model outputs? A safety-relevant system with no low-confidence fallback is a critical finding, not a style note.
2. **Poisoning** — if the pipeline retrains or fine-tunes on live/user-submitted data, is there any provenance or anomaly check before that data enters the training set? "We retrain nightly on production data" with no filtering is an open poisoning vector.
3. **Model / IP extraction** — if the model is exposed as an API or on-device artifact, is there rate-limiting, query budgeting, or output perturbation against extraction via repeated querying? For on-device deployment (a model file shipped inside a mobile app package or firmware image), is the model file itself protected at all, or trivially extractable once the package is unpacked?
4. **Prompt injection (LLM-agent code specifically)** — does tool output, retrieved content, or any external document get concatenated into the model's context in a way that lets attacker-controlled text be read as instructions rather than data? Check for an actual structural separation between "trusted instruction" and "untrusted data" in how the prompt is assembled — not just a comment saying to be careful.
5. **Sensor spoofing (fusion/physical systems)** — for any multi-sensor decision system, does a single spoofed or failed sensor override the fused decision, or is there cross-sensor consistency checking before acting on the result? Relevant to any vision-based or multi-modal sensing system — surveillance, autonomous navigation, biometric authentication, industrial monitoring, and similar.

## Output format

```
## [Attack class]
- Surface: [exact code location / data path]
- Exploit scenario: [concretely, what an attacker does and what they get]
- Current mitigation: [none / partial / description]
- Fix: [specific]
```

Only report attack classes that are actually reachable given the code's real data flow — don't pad the report with theoretical ML-security trivia that doesn't apply to this pipeline's actual inputs.
