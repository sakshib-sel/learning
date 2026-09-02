# Week 2 Check

Run the local Week 2 validation checks.

```bash
python3 -m unittest discover -s tests
sentinel-claude validate-json week-2/examples/valid-analysis.json
```

Then summarize whether the app can parse valid output, reject invalid output,
and reject interrupted streams.

