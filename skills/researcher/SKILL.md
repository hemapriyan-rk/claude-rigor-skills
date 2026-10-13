---
name: researcher
description: Adversarial technical research that tries to break the claim, not confirm it. Covers papers, patents, shipped products, and standards, with a search budget sized to the stakes. Use to check prior art, map the state of the art, or validate a claim before committing to it. Not for one-fact lookups.
---

# Researcher

Most research fails because it searches to confirm, not to falsify. This skill produces research that survives a patent examiner, a peer reviewer, or a skeptical cofounder, and spends only as many searches as the decision is worth.

## 1. Scope and budget

Before any search, write down:

- **The claim being tested,** stated so it can be false: "A system that does X using Y under constraint Z doesn't exist," not "is my idea good?"
- **What would kill it:** the specific evidence that would make the claim false. If you can't name it, you don't understand the claim yet.
- **The search budget,** based on what the answer will decide:

| Stakes | Budget | Example |
|---|---|---|
| **Quick** | up to 5 searches, 2 page reads | Is this idea worth an afternoon? |
| **Standard** | up to 15 searches, 6 page reads | Choosing an approach for a project |
| **Deep** | up to 40 searches, 15 page reads | Patent filing, paper submission, months of work |

Default to **Standard** unless the user says otherwise. Say which budget you're using.

**Stop early** when you find the kill evidence (report it), or when every relevant layer has been searched and fresh queries only return sources you've already seen.

Read `references/sources.md` from this skill's base directory before the first search. It lists where to search for each layer and how to build queries.

## 2. Search every layer that matters

Skipping a layer is the most common way research gets blindsided. Cover the ones relevant to the claim:

- **Academic:** papers and preprints.
- **Patents:** required whenever novelty is even part of the question. Patents rarely show up in plain web search.
- **Shipped products and open source:** what actually exists and works, as opposed to what was published.
- **Standards and regulation:** when the domain has them.

## 3. Search for the kill

After a favorable first pass, spend part of the budget trying to break the conclusion. Search with the words a competitor or examiner would use, describing the **mechanism**, not the user's own terms. Different names for the same thing hide the closest prior art from naive searches.

## 4. Double-source what the conclusion rests on

Find the two or three claims the conclusion depends on. Each needs two independent sources. Mark everything else as single-sourced.

## Output

```
# Research: <topic>
Budget: <Quick / Standard / Deep>, <n> searches used.

## Claim tested
## What would falsify it (stated before searching)

## Closest existing work
| Source (dated) | Type | Mechanism | How close | Gap vs. the claim |

## Strongest counter-evidence
<the best evidence against the claim, or "none found" plus which layers and queries were checked>

## Verdict
<supported / weakened / killed>, in one or two sentences, with confidence and why.

## Open questions
## Sources (dated, grouped by type)
```

Rules for the write-up:

- Don't treat marketing pages or a company's claims about itself as verified fact.
- "No counter-evidence found" must say how hard you looked.
- Hand the result to `researcher-evaluator` for a second pass when the stakes are Deep.
