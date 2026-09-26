---
name: ieee-paper-drafter
description: Draft an IEEE-conference/journal-style research paper — full section structure, IEEE numeric citation style, and a ready IEEEtran LaTeX skeleton — with the same rigor bar a reviewer would apply. Use whenever the user wants to write up a research idea, project, or result as an IEEE-format paper, or asks for an abstract/related-work/methodology section in that style. Do not use this for informal write-ups or blog-style summaries — that's plain markdown, not this skill.
---

# IEEE Paper Drafter

A paper that reads well to its author and a paper that survives peer review are different documents. The gap is almost always: omitted limitations, a related-work section that lists instead of compares, and improvement claims without a stated baseline. This skill exists to close that gap before submission, not after rejection.

## Step 1 — Use the template

Copy `assets/ieee_template.tex` as the starting file (standard `IEEEtran` conference class, ready to compile). It has the full section skeleton with inline comments on what each section actually needs — follow the section order; it matches reviewer expectations and deviating from it invites confusion, not creativity points. If the user wants a `.docx` instead of LaTeX, use the `docx` skill for the file mechanics but keep the same section structure and rigor rules below.

## Step 2 — Section-by-section rigor rules

- **Abstract**: self-contained, 150-250 words, no citations, includes the single strongest result as an actual number — not "significant improvement," but "X% reduction in Y." Every superlative in the abstract must be backed by a metric stated later in the paper.
- **Introduction**: state the specific mechanism of failure in existing approaches, not "prior work has limitations." List contributions as explicit bullets — a reviewer scanning for contributions should not have to infer them from prose.
- **Related Work**: must compare mechanisms against the nearest competing work, not just cite and summarize each one in isolation. Run the `researcher` skill to find the actual closest work if it isn't already identified, then the `researcher-evaluator` skill against this section specifically — an incomplete or list-style related-work section is the most common reason a technically sound paper gets rejected on presentation grounds.
- **Proposed Method**: enough detail for a reader with no code access to reproduce it. Define every symbol before using it. State non-obvious design decisions and name the rejected alternative and why — this preempts the review comment "why not X instead."
- **Experimental Setup**: baselines must include the strongest real competitor found during related-work research, not an easy strawman — a paper that only beats a weak baseline gets flagged immediately by any competent reviewer.
- **Results and Discussion**: report negative and limiting results, not just the wins. Every claimed improvement needs the specific metric and the specific baseline it beat, stated together, not separated across paragraphs.
- **Limitations**: an explicit section, not a buried caveat. State plainly what the method does not solve and under what conditions it breaks — reviewers penalize omitted limitations far more heavily than disclosed ones.
- **Conclusion**: restate the contribution against the original problem, not a generic "we presented a novel approach" — that sentence is a reliable signal to reviewers that the author isn't sure what the actual contribution was.

## Step 3 — Citation discipline

IEEE style is numeric, ordered by first appearance in text (`[1]`, `[2]`, ...), with the reference list in that same order — not alphabetical. Each reference entry: author initials, title in quotes, venue, year, page range. Never cite a source for a claim stronger than what that source actually supports — this is the single fastest way to lose reviewer trust once caught.

## Step 4 — Before calling it done

Run the `researcher-evaluator` skill against the Related Work and Results sections specifically, since those are where unsupported or miscalibrated claims do the most damage. A paper with a strong method section and a weak related-work section still gets rejected — reviewers judge the comparison, not just the contribution in isolation.
