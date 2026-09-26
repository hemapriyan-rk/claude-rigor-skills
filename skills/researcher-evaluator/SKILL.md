---
name: researcher-evaluator
description: Stress-test a piece of research — a report, literature review, competitive analysis, or "I looked into it and..." summary — for rigor, bias, and hidden gaps before it gets relied on. Use whenever the user shares research (their own, another AI's, or a document) and asks whether it holds up, whether they missed something, or whether a conclusion is safe to act on. Give a blunt verdict, not a polite summary. Do not use this for grading writing style — this is about evidentiary rigor only.
---

# Researcher Evaluator

Research is easy to produce and easy to make look convincing. This skill's only job is to find where it's actually load-bearing versus where it's decoration, and say so without softening it.

## Read the whole artifact first

Read the full research output — every claim and every source — before forming a verdict. Don't sample the executive summary and extrapolate.

## Run this checklist against it

1. **Source quality** — Is each claim backed by a primary source (paper, patent, official docs, company's own filing) or by an aggregator/blog/marketing page restating something else? Flag every load-bearing claim resting only on a secondary source.
2. **Recency** — Does every claim about "current state" carry a date, and is that date actually recent enough to matter for a fast-moving domain? A 2022 claim about "the state of the art" in ML is often already wrong.
3. **Coverage, not just volume** — Did the search actually cover the layer that could falsify the conclusion (patents, if novelty is claimed; shipped products, if "nothing like this exists" is claimed), or did it only search the layer that was easy and reassuring?
4. **Cherry-picking** — Is there a search for disconfirming evidence at all, or does the report read like it stopped the moment it found support? Absence of counter-evidence in the report is not the same as absence of counter-evidence in the world — check whether the report distinguishes the two.
5. **Confidence calibration** — Does the language's certainty match the actual evidence strength? "Definitely novel" backed by three quick searches is miscalibrated; flag every overclaim.
6. **Load-bearing claims, individually** — Identify the 2-3 claims the final conclusion actually depends on. Each needs independent double-sourcing. If any of them has only one source, the conclusion is not yet safe to act on, regardless of how much other material surrounds it.
7. **Reproducibility** — Could someone re-run the described searches and land on the same picture, or is the trail too vague to check (no query terms, no source list, just conclusions)?

## Verdict

Give one of three verdicts, stated plainly:

- **Solid** — load-bearing claims are double-sourced, disconfirming search was actually attempted and came up empty, confidence matches evidence.
- **Shaky** — usable as a starting point, but named gaps must be closed before anyone acts on it.
- **Trash** — the conclusion isn't supported by what was actually checked; don't act on this as-is.

For every failure found, give:
- what's wrong (one line, specific — not "sourcing could be better")
- the exact fix — the specific search query, source type, or reference still missing

Never round a weak result up to "mostly fine" to soften delivery. The point of this skill is that the verdict is the same whether it's flattering or not.
