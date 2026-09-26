---
name: patent-drafter
description: Draft a full patent specification — background, summary, detailed description, and a claim ladder (independent + dependent claims) — for an invention. Use whenever the user asks to draft a patent, write patent claims, or turn an invention into a filing-ready-style document. Requires (or produces, if missing) a novelty check first — drafting polished claims around something already anticipated by prior art wastes effort, so this skill will not silently skip that step. Produces a technical working draft for attorney review, not a filed legal document.
---

# Patent Drafter

A patent draft's value is almost entirely in the claims, and claim quality depends entirely on knowing exactly what prior art it has to clear. Drafting without that is just writing an essay in patent-shaped font.

## Step 0 — Confirm a novelty check has happened

Before drafting claims, check whether the closest prior art has already been identified (via the `patent-novelty-evaluator` skill, or supplied by the user). If not, say so directly and either run that check first or draft with an explicit, visible caveat that Claim 1's scope is provisional until prior art is confirmed. Never draft a claim ladder that silently assumes no prior art exists.

## Step 1 — Use the template

Copy `assets/patent_spec_template.md` as the starting file. It has the standard section skeleton (Field, Background, Summary, Drawings, Detailed Description, Claims, Abstract) with the drafting rules for each section already annotated. Fill it in — don't restructure it; the section order and the annotations exist for reasons specific to patent prosecution, detailed below.

## Step 2 — Drafting rules that actually matter

- **Background**: describe the problem and prior art's shortcomings functionally. Never characterize prior art more broadly than necessary — every sentence here is a potential admission usable against claim scope later.
- **Detailed Description must be enabling**: a person of ordinary skill in the art must be able to build/practice the invention from this section alone. Every term that appears in a claim must be supported here — an unsupported claim term is a written-description vulnerability, not a stylistic nitpick.
- **Claim 1 (independent) breadth**: draft it exactly as broad as the closest prior art found allows — no broader (invites rejection/invalidation) and no narrower (gives up defensible scope and commercial value for nothing). This is where the novelty check output gets used directly: the distinguishing element in Claim 1 should be the minimum limitation that clears the specific closest reference.
- **Dependent claims are fallback positions, not restatements**: each one should narrow the claim by one real limitation that would still make the invention worth having if the independent claim gets rejected or invalidated later. A dependent claim that just repeats the independent claim's language with a synonym is wasted.
- **Consider both a method claim set and a system/apparatus claim set** covering the same invention when both are viable — this is a standard hedge, not padding, since infringement analysis differs by claim type.
- **Abstract**: describes the disclosure, not the pitch. Superlatives ("novel," "superior," "groundbreaking") get flagged by examiners as advertising and should not appear here or anywhere in the claims.

## Step 3 — Run the checklist at the bottom of the template before presenting the draft

Every box on that checklist is a real prosecution risk, not busywork — confirm each one explicitly rather than assuming it's fine.

## Always state plainly

This produces a technical working draft to accelerate attorney review — it is not legal advice and is not filing-ready. Say this once, clearly, without turning it into a disclaimer wall that buries the actual draft.
