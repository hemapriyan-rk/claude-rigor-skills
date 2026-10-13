---
name: patent-novelty-evaluator
description: Stress-test an invention for patentability (novelty, inventive step, subject-matter eligibility, claim scope) against the closest prior art found. Gives a blunt verdict: dead on arrival, weak, or defensible. Use for "is this patentable?" or to re-check a draft claim. Technical analysis, not legal advice.
---

# Patent Novelty Evaluator

Most inventions that feel novel are novel only relative to what the inventor happened to search. This skill finds the prior art that would kill the claim, and says so plainly if it does.

## 1. Scope and budget

- **Extract the claim skeleton first,** before searching:
  - the problem solved;
  - the mechanism: *how* it works, not the goal;
  - the single element believed to be new.

  If the "new" element is really "known technique X applied to domain Y," say so now. It's the most common failure for software and AI patents.
- **Ask for the target jurisdiction** (US, Europe, India, or other) if it isn't given, and default to US and Europe. The legal tests differ.
- **Search budget:** up to 15 searches and 6 full documents read by default; up to 30 and 12 if the user is preparing to file. **Stop early** once one reference discloses every element of the claim. That settles novelty, and further searching won't change the verdict.
- **Load the references before searching.** Read `references/patent-search.md` and `references/legal-tests.md` from this skill's base directory in the same step.

## 2. Search for prior art

Cover all three, using the search guide:

- **Patents:** by mechanism keywords and by CPC class.
- **Non-patent literature:** papers, preprints, standards.
- **Products:** shipped devices, open-source code, datasheets. These are prior art too, and the layer most often missed.

## 3. Pick the closest reference

Name the one reference, or the smallest combination, that comes closest. A list of twenty loosely related patents isn't an answer.

## 4. Run the tests

Use `references/legal-tests.md` for the target jurisdiction.

1. **Novelty:** compare element by element against the closest reference. If one reference discloses every element, the claim is anticipated.
2. **Inventive step / non-obviousness:** would a skilled person combine the closest reference with another known one to get the claim, expecting it to work? Is there an unexpected technical effect?
3. **Eligibility:** is this an abstract idea or algorithm on generic hardware, or a specific technical improvement?
4. **Claim scope:** is it too broad (more prior art in reach) or too narrow (easy to design around)? Name the element to add or remove.

## Output

State the verdict first.

```
## Verdict: Dead on arrival | Weak (needs rework) | Defensible as drafted
<one or two sentences: why>

## Claim skeleton
## Closest prior art
<reference, date, what it discloses>

## Element-by-element comparison
| Claim element | Closest reference | Disclosed? |

## Inventive step
## Eligibility (<jurisdiction>)
## How to strengthen the claim
<the specific narrowing or technical effect that would help, if any>

## Search log
<databases, queries, CPC classes, number of documents reviewed>
```

Never round "weak" up to "defensible" to be encouraging. End with one line: this is a technical assessment, not legal advice, and a patent attorney should review before any filing decision.
