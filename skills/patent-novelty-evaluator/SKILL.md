---
name: patent-novelty-evaluator
description: Stress-test an invention for patentability — novelty, inventive step/non-obviousness, subject-matter eligibility, and claim scope — before time or money goes into filing. Use whenever the user describes an invention, a patent claim, or a "is this patentable" question, or asks to re-evaluate an existing patent draft or provisional. Gives a blunt kill/weak/defensible verdict backed by the closest prior art found, not a generic "sounds novel" reassurance. This is technical prior-art and claim analysis, not legal advice — a patent attorney should confirm before filing.
---

# Patent and Novelty Evaluator

Most inventions that feel novel to their inventor are novel only relative to what the inventor happened to search. This skill's job is to find the prior art that would actually kill the claim, and say so plainly if it does.

## Step 1 — Extract the claim skeleton before searching anything

Force the invention into claim form first, even roughly:
- The problem being solved.
- The structure or method (the actual novel mechanism — not the goal, the *how*).
- The single element the applicant believes is the distinguishing contribution.

If the "distinguishing contribution" is vague or is really just "applying known technique X to new domain Y," flag that immediately — it's the most common software/AI patent failure mode and worth naming before spending a search budget on it.

## Step 2 — Prior art search (see the `researcher` skill for search methodology)

Cover, at minimum:
- **Patent literature**: Google Patents, Espacenet, WIPO PatentScope, USPTO full-text — search by mechanism/function, not just the applicant's own vocabulary. This is non-negotiable; skipping patent search is not a novelty search.
- **Non-patent literature**: papers, preprints, standards docs describing the same mechanism.
- **Commercial prior art**: shipped products, open-source repos, datasheets doing the same thing in practice, even without a patent behind them — these count as prior art too and are frequently missed.

## Step 3 — Pick the closest reference(s), not a pile of tangential ones

Identify the single closest piece of prior art (or the smallest combination of references). A report listing twenty loosely-related patents without naming which one is actually the threat is not useful — narrow to the one that matters.

## Step 4 — Novelty test (anticipation)

Element-by-element comparison against the closest reference: does it disclose every element of the claim, even if described in different words? If yes, the claim is **anticipated** — dead as drafted, full stop, no amount of enthusiasm changes it. State this directly if it's the case.

## Step 5 — Inventive step / non-obviousness test

If not anticipated by a single reference, check obviousness via combination:
- Would a person skilled in the art, aware of the closest reference plus the other found references, arrive at the claimed invention through routine work, with a reasonable expectation of success?
- Was there a motivation to combine the references (or does the art actually teach away from combining them)?
- Is there an unexpected result — a benefit not predictable from the individual references — that would support non-obviousness?

Name explicitly if the claim is "known technique A + known technique B, combined in an unsurprising way, in a new but foreseeable application" — this is the single most common reason software/AI/sensor patents get rejected or invalidated, and it should be called out as such rather than danced around.

## Step 6 — Subject-matter eligibility (especially for software/AI/algorithmic claims)

Flag eligibility risk when the claimed invention is really an abstract idea, algorithm, or mental process dressed up with generic hardware ("a processor configured to..."), rather than tied to a specific technical improvement (e.g., a measurable gain in system performance, a physical sensing mechanism, a concrete technical effect). This is where AI/software patents die most often even when technically novel. Note explicitly when this risk applies — it's a distinct failure mode from novelty and obviousness.

## Step 7 — Claim scope check

- **Too broad**: invites both rejection (more prior art in scope) and later invalidation.
- **Too narrow**: easy to design around, low commercial value even if granted.
State which direction the current framing errs in, and the specific element that should be added (to narrow) or removed (to broaden) to fix it.

## Verdict — always one of three, stated first

- **Dead on arrival** — anticipated by a specific found reference. Name the reference.
- **Weak — needs narrowing/rework** — survives anticipation but has a real obviousness or eligibility problem; name the fix that would address it.
- **Defensible as drafted** — closest art identified, doesn't anticipate, inventive step holds, eligibility risk low. Still name the closest reference found, so it's on record for the actual filing.

Never round "weak" up to "defensible" to be encouraging. State clearly that this is a technical assessment, not legal advice, and that a patent attorney should review before any filing decision — this changes the confidence framing, not the bluntness of the technical verdict itself.
