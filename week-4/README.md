# Week 4 -- Measuring And Optimizing Sentinel

Week 4 turns Sentinel into a measured system. The focus is evaluation,
model/configuration selection, cost, prompt caching, batching, and context
engineering.

Because the Anthropic key currently authenticates but cannot run generation due
to insufficient credits, live model calls are not invented. Week 4 uses a
deterministic evaluation simulator so the workflow remains repeatable.

## Run

```bash
python3 -m pip install -e .
sentinel-evaluate --configuration baseline --output outputs/week-4/baseline-eval.json
sentinel-evaluate --configuration optimized --output outputs/week-4/optimized-eval.json
sentinel-cache-sim --output outputs/week-4/cache-hit.json
sentinel-cache-sim --change system_prompt --output outputs/week-4/cache-invalidation.json
sentinel-batch-sim --output outputs/week-4/batch-sim.json
```

## Quality Threshold

The required quality threshold is `0.8`. An optimization is accepted only if it
meets the threshold and does not introduce unacceptable behavioural regression.

## Deliverables

See `submission.md`.

