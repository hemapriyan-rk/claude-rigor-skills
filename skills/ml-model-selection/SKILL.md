---
name: ml-model-selection
description: Choose the right ML model architecture, size, and family for a task given real constraints — latency ceiling, accuracy floor, compute/memory budget, and deployment target (cloud vs. edge/on-device) — instead of defaulting to the largest or most fashionable model. Use whenever picking a model for a new pipeline, or reconsidering one that's too slow, expensive, or large for its actual deployment target.
---

# ML Model Selection

Picking the largest available model and calling it a safety margin is picking on vibes, not evidence. This skill forces the constraints to be numbers first, and treats "biggest that fits" as a real trade-off decision, not a default.

## Step 1 — State constraints as numbers before looking at any model

Latency ceiling, accuracy floor, and compute/memory budget. If the deployment target is edge or on-device, tie the budget to the `embedded-constrained-coding` skill's numbers (actual RAM/flash/power figures for the target) rather than assuming cloud-class headroom. State plainly if the target simply can't run a large model at all — that rules out entire classes before wasting time evaluating them.

## Step 2 — Don't default to the largest or newest model

State the actual task complexity: does this problem genuinely need a large general-purpose model, or does a smaller, specialized/fine-tuned model already clear the accuracy floor at a fraction of the cost? A model that clears the bar by far more than the floor requires isn't a safety margin — it's wasted latency and compute budget that has to be paid on every inference.

## Step 3 — Check what's actually available at the target size

Consider smaller open models, distilled variants, and — for a well-structured problem — a classical (non-deep-learning) baseline that might already clear the accuracy floor. A classical model hitting 90% of the target metric at 1% of the compute is often the right call, not the lesser one; don't dismiss it just because it's less fashionable.

## Step 4 — Quantization/distillation fit, checked not assumed

If the best-fit model still exceeds budget, check what quantization or distillation actually does to the accuracy floor before assuming "it should still be fine" — this needs the same measured verification `embedded-constrained-coding` requires, not an estimate.

## Step 5 — Verify against data that matches the real deployment distribution

Evaluate on a held-out set drawn from the actual deployment distribution, not just the benchmark the model is famous for. A model selected on a benchmark score that doesn't reflect the real input distribution (sensor noise, population, environment) is a decision made on the wrong evidence — this is the same distribution-match check the `dataset-sourcing` skill runs, applied here to model evaluation instead of dataset choice.

## Output

```
# Model selection: [task]
## Constraints (latency / accuracy / compute-memory budget / deployment target)
## Candidates (2-3), each with: accuracy, latency, memory, cost against a matching-distribution eval
## Recommendation, and the specific reason the runner-up(s) were rejected
```
