# Week 4 Check

Run the local Week 4 validation checks.

```bash
python3 -m unittest discover -s tests
sentinel-evaluate --configuration baseline
sentinel-evaluate --configuration optimized
sentinel-cache-sim
sentinel-cache-sim --change system_prompt
sentinel-batch-sim
```

Summarize whether the optimized configuration meets the threshold without
introducing forbidden claims, and whether cache and batch simulations behave as
expected.

