# Prompt Caching

The app marks the stable Sentinel system contract with ephemeral cache control.

Experiment:

```bash
sentinel-claude analyze --incident week-1/incidents/INC-104.md --model claude-sonnet-5
sentinel-claude analyze --incident week-1/incidents/INC-107.md --model claude-sonnet-5
```

Record:

| Request | Cache creation tokens | Cache read tokens | Uncached input tokens | Latency | Estimated cost |
| --- | ---: | ---: | ---: | --- | ---: |
| Stable contract + INC-104 |  |  |  |  |  |
| Stable contract + INC-107 |  |  |  |  |  |

If the model, account, or prompt length does not support caching, record that
limitation rather than inventing results.

## Concepts

- Prompt caching stores reusable prompt prefixes for cheaper/faster reuse.
- KV cache is the model-serving runtime's internal attention cache.
- Conversation history is prior messages sent again as part of the request.
- Application memory is data the app stores and chooses to include later.

