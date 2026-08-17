# Week 1 -- A Convincing AI Answer Can Still Be Unsafe

## Objective

Learn how language models generate plausible responses, why confident answers
are not necessarily correct, and how to evaluate AI-generated incident analysis
using evidence and uncertainty.

## Activities

1. Paste the full `INC-104` incident into `incidents/INC-104.md`.
2. Complete `notes/pre-model-analysis.md` before using a model.
3. Run the baseline prompt at least five times and record results in
   `experiments/baseline-runs.md`.
4. Run the zero-shot, one-shot, and few-shot prompts without changing the
   incident, model, or generation settings.
5. Compare prompt variants in `experiments/prompt-comparison.md`.
6. Capture facts, assumptions, hypotheses, missing evidence, and unsupported
   claims in `notes/facts-assumptions-hypotheses.md`.
7. Finish `notes/reflection.md`.

## Completion Gate

Week 1 is complete when the evidence tables are filled from actual model runs
and the final reflection explains:

- why lower temperature does not guarantee correctness
- why structure does not guarantee factuality
- what evidence is missing before recommending action
- what Sentinel can and cannot safely conclude

