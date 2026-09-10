# Model Selection Decision

As of September 10, 2026, Anthropic's deprecation documentation lists active
models including `claude-sonnet-5`, `claude-opus-5`, `claude-fable-5`, and
current 4.x variants. The Week 2 API key test also returned Sonnet 5, Opus 5,
and Fable 5 model IDs.

| Workload | Recommended configuration | Reason |
| --- | --- | --- |
| Interactive incident triage | `claude-sonnet-5`, direct or fast mode | Balanced quality, latency, and cost. |
| High-risk evidence review | `claude-opus-5` or Sonnet with thinking/effort enabled | Prefer quality and careful evidence separation over speed. |
| High-volume offline summarization | Haiku/Fable-class model through Message Batches | Lower urgency and volume favor cost efficiency. |
| Low-latency classification | Fast mode on a smaller model | Short outputs and simple labels do not need expensive reasoning. |

## Thinking Trade-Offs

- Fast mode favors latency and cost.
- Extended thinking can improve difficult reasoning but costs more tokens and
  latency.
- Adaptive thinking lets the model decide when deeper reasoning is needed.
- Effort controls tune reasoning depth where supported.

More thinking does not create evidence that is missing from the incident.

