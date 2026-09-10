# Token And Cost Worksheet

Approximate Sonnet-class prices used by the simulator:

| Token type | Price |
| --- | ---: |
| Input | $3.00 / MTok |
| Output | $15.00 / MTok |
| Cache read | $0.30 / MTok |

Formula:

```text
cost = input_tokens / 1,000,000 * input_price
     + output_tokens / 1,000,000 * output_price
     + cache_read_tokens / 1,000,000 * cache_read_price
```

Worst-case planning should use maximum tool calls, maximum output tokens, and no
cache hit.

Normal-case planning may use measured averages from `outputs/week-4/`.

