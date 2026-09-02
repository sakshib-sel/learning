# Model Selection And Thinking

## Model Tiers

| Tier | Trade-off |
| --- | --- |
| Haiku | Lower cost and latency, lower capability for difficult reasoning. |
| Sonnet | Balanced quality, latency, and cost. Good default for Sentinel. |
| Opus | Highest capability, higher cost and latency. Best for difficult cases. |

## Direct Vs Thinking

Direct response:

```bash
sentinel-claude analyze --incident week-1/incidents/INC-104.md --model claude-sonnet-5
```

Thinking-enabled response:

```bash
sentinel-claude analyze \
  --incident week-1/incidents/INC-104.md \
  --model claude-sonnet-5 \
  --thinking-budget-tokens 1024
```

## Comparison Notes

More thinking may improve hypothesis separation and missing-evidence
identification, but it does not create evidence that is absent from the
incident. A thinking response must still avoid unsupported root-cause claims.

