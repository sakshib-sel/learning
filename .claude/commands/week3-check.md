# Week 3 Check

Run the local Week 3 validation checks.

```bash
python3 -m unittest discover -s tests
sentinel-tool-loop --incident week-1/incidents/INC-104.md
```

Summarize whether the mocked tool loop obtains bounded evidence, rejects unsafe
requests, treats tool results as untrusted data, and terminates within limits.

