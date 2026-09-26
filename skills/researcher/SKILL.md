---
name: researcher
description: Conduct deep, adversarial technical research — prior art, state-of-the-art, competitive landscape, standards — for patents, papers, architecture decisions, or any claim that needs to survive scrutiny. Use whenever the user asks to research a technical topic, check if something already exists, find prior art, scope a literature review, or validate a technical/market claim before committing to it. Do not use for quick single-fact lookups — this is for multi-source, defensible research where being wrong is expensive.
---

# Researcher

Most "research" fails for one reason: it searches to confirm, not to falsify. This skill exists to produce research that survives someone actively trying to break it — a patent examiner, a peer reviewer, a competitor's lawyer, a skeptical cofounder.

## Step 1 — Scope before searching

Pin down, in writing, before running any search:
- The exact claim or question being tested (not "is my idea good" — "does a system with properties X, Y, Z already exist, and if a close variant exists, what exactly differs").
- The domain boundaries (industry, geography, time window — a 2019 paper doesn't tell you what shipped in 2026).
- What would count as a **kill** — the single strongest form of prior art or counter-evidence that would invalidate the premise. Name it before searching for it. If you can't name what would kill the claim, you don't understand the claim yet.

## Step 2 — Search across every layer that matters, not just the easy one

Skipping a layer is the single most common way research gets blindsided later. Cover what's relevant to the question:

- **Academic**: arXiv, IEEE Xplore, ACM DL, Google Scholar — for SOTA techniques and named prior work.
- **Patents**: Google Patents, Espacenet, WIPO PatentScope, USPTO full-text search — required whenever novelty or patentability is even adjacent to the question. A literature search with no patent search is not a novelty search; patents are often the closest prior art and never show up in a plain web search.
- **Commercial / shipped product**: company docs, changelogs, GitHub repos, press releases, app store listings, Show HN / Product Hunt. Papers describe what was published; products describe what actually exists and works. Both matter, separately.
- **Standards / regulatory**: relevant when the domain has one (medical devices, safety systems, telecom, etc.) — these often constrain what's viable regardless of technical novelty.

Scale the number of searches to how much rides on the answer. A throwaway question gets a few searches. A patent claim or an architecture decision that will take months to build gets as many searches as it takes to either find the killer reference or convince yourself it's genuinely not out there.

## Step 3 — Deliberately search for the kill, not just supporting evidence

After the first pass looks favorable, run a second pass whose only goal is to break it: search using the vocabulary a competitor, examiner, or reviewer would use, not the vocabulary the user used to describe their own idea. Different naming conventions hide the closest prior art from naive searches constantly — search by mechanism and function, not just by the user's chosen terminology.

## Step 4 — Verify load-bearing claims twice

Identify the 2-3 claims the whole conclusion actually depends on. Each of those needs at least two independent sources, not one source cited twice. Everything else can be single-sourced and flagged as such.

## Output structure

```
# Research: [topic]

## Question / claim being tested
## What would falsify this (stated up front, before results)

## Prior art & existing solutions
| Source | Mechanism | How close | Gap vs. the idea |

## State of the art (non-competing techniques worth knowing)

## Strongest counter-evidence found
(if none found, say so explicitly and say how hard you looked — "checked X, Y, Z layers" — don't imply absence of evidence is evidence of absence without showing the work)

## Open gaps / unresolved questions

## Sources
(dated, layered by type — patent / paper / product / standard)
```

## Anti-patterns to avoid

- Reporting only sources that agree with the premise.
- Treating marketing copy or a company's own claims as verified fact.
- Citing a single source for a claim the whole conclusion rests on.
- Stopping the search the moment something reassuring turns up.
- Presenting search-engine confidence as domain confidence — a thin result set means "look harder or say it's inconclusive," not "probably fine."

Hand off the output to the **researcher-evaluator** skill for a second, adversarial pass before treating it as settled — you wrote it, you're the worst-positioned judge of your own blind spots.
