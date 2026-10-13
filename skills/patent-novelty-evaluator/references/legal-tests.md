# Patentability tests by jurisdiction

A technical summary to structure the analysis. Not legal advice. Laws and case law change, so confirm with a patent attorney before relying on it.

## Novelty

| Jurisdiction | Basis | Test |
|---|---|---|
| **US** | 35 U.S.C. § 102 | A single prior-art reference must disclose every element of the claim, explicitly or inherently |
| **Europe (EPO)** | Article 54 EPC | The claimed subject matter must not be part of the state of the art; a single document must disclose all features directly and unambiguously |
| **India** | Section 2(1)(j) and (l), Patents Act 1970 | The invention must not be anticipated by publication or use before the priority date |

## Inventive step / non-obviousness

| Jurisdiction | Basis | How it's assessed |
|---|---|---|
| **US** | 35 U.S.C. § 103 | Graham factors: scope and content of the prior art, differences from the claim, level of ordinary skill, and secondary considerations (commercial success, long-felt need, failure of others). After *KSR v. Teleflex* (2007), combining known elements with predictable results is likely obvious |
| **Europe** | Article 56 EPC | Problem-solution approach: (1) pick the closest prior art, (2) find the distinguishing features and their technical effect, (3) frame the objective technical problem, (4) ask whether the skilled person *would* (not just *could*) have arrived at the solution |
| **India** | Section 2(1)(ja) | A technical advance over existing knowledge, or economic significance, or both, that is not obvious to a person skilled in the art |

## Subject-matter eligibility

| Jurisdiction | Basis | Test |
|---|---|---|
| **US** | 35 U.S.C. § 101 | *Alice/Mayo* two steps: (1) is the claim directed to an abstract idea, law of nature, or natural phenomenon? (2) if so, do the additional elements add "significantly more," such as a specific improvement to computer functionality or another technology? |
| **Europe** | Article 52(2)–(3) EPC | Programs, mathematical methods, and business methods are excluded "as such." A claim involving technical means passes the first hurdle, but only features with a technical effect count toward inventive step |
| **India** | Section 3(k) | "A mathematical or business method or a computer programme per se or algorithms" is not an invention. Software claims need a technical effect or contribution beyond the program itself |

## Common failure patterns

- **Known technique, new domain:** applying an existing ML model or algorithm to a new field, with no technical change to how it works.
- **Aggregation:** combining known parts that each do what they always did, with no interaction that produces a new effect.
- **Result, not mechanism:** claiming the goal ("detects fatigue accurately") instead of the specific way it's achieved.
- **Generic hardware:** "a processor configured to…" wrapped around an algorithm, with no improvement to the hardware or system itself.
