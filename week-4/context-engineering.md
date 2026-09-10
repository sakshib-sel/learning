# Context Engineering

Compare four strategies:

| Strategy | Benefit | Risk |
| --- | --- | --- |
| Full unfiltered context | Maximum detail | High cost, latency, and context drift |
| Pruned tool results | Lower token use | May remove useful detail |
| Typed context compaction | Keeps critical evidence in stable fields | Requires careful schema discipline |
| Separate review stage | Isolates high-risk review | More steps and latency |

Optimized context must preserve:

- evidence identifiers
- negative findings
- contradictions
- unresolved uncertainty
- source attribution
- decisions already made

Helpers live in `src/sentinel_claude/context_engineering.py`.

