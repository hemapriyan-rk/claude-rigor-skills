---
name: dataset-sourcing
description: Find and evaluate datasets for training or validating a model — checking license, quality, leakage risk, bias, and whether the dataset's actual distribution matches the real deployment domain. Use whenever a project needs training or validation data, and before treating any found dataset as ready to use as-is.
---

# Dataset Sourcing

A benchmark dataset that doesn't match the real deployment distribution will produce a model that looks great in evaluation and fails in the field — this is the single most common way ML projects quietly fail. This skill checks the match, not just the existence, of candidate datasets.

## Step 1 — Define the real deployment distribution first

Before searching, state what real input actually looks like in production: sensor noise characteristics, real-world class balance, the actual environmental/population variation the deployed system will see. A dataset search with no stated acceptance criteria isn't a search, it's browsing.

## Step 2 — Search across the layers that matter

- Domain-specific benchmark datasets for the exact task.
- Adjacent-domain datasets that could transfer, when nothing matches exactly.
- Where nothing fits well: what it would actually take to collect or synthesize a small, correctly-distributed set instead of forcing a mismatched public dataset to work. Naming this option explicitly matters even when it isn't chosen — it's the honest alternative to a bad-fit shortcut.

## Step 3 — License check, before anything else

Commercial-use restrictions, attribution requirements, share-alike terms that could constrain what the resulting model is allowed to be used for. Flag immediately if a dataset that otherwise fits well has a license that blocks the intended use — this needs to surface before time is spent on it, not after.

## Step 4 — Quality and leakage check

- Duplicate or near-duplicate entries between train and test splits — a common, silent inflator of reported accuracy that makes a model look better than it is.
- Label noise rate, if knowable from documentation or spot-checking.
- Shortcut risk — does the collection process introduce an artifact a model could learn instead of the real signal (e.g., all positive examples sharing an unrelated visual or metadata artifact)? This is worth an explicit check, not an assumption that a well-known dataset is clean.

## Step 5 — Distribution match against Step 1

Compare the dataset's actual distribution (class balance, input characteristics, collection conditions) against the real deployment distribution stated in Step 1. State the gap explicitly rather than assuming a benchmark generalizes to a different physical sensing setup, population, or environment — this is the check most often skipped and most responsible for field failures.

## Step 6 — Bias check

Check whether the dataset underrepresents conditions, classes, or populations that matter for the deployment context. For anything safety- or identity-related (medical diagnosis, autonomous systems, biometric authentication), a representation gap here is a real-world failure mode, not a fairness footnote to mention and move past.

## Output

```
# Dataset candidates: [task]
| Dataset | License | Size | Distribution match vs. deployment | Known gaps |

## Recommendation: usable as-is / usable with [specific augmentation] / not usable — collect instead, because [reason]
```
