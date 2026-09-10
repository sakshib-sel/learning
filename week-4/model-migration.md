# Model Migration Safety

Changing model or thinking configuration is a behavioral change.

Experiment:

- Baseline: full context, no cache, direct Sonnet-class response.
- Optimized: typed compaction, prompt-cache simulation, shorter output target.

Observed deterministic result:

| Area | Baseline | Optimized |
| --- | --- | --- |
| Output structure | Mostly valid, one failure on timestamp conflict | Valid across fixed cases |
| Fact preservation | Failed one timestamp-conflict fact | Preserved expected facts |
| Tool selection | Adequate | Adequate |
| Reasoning behavior | Over-weighted deployment in INC-109 | Preserved uncertainty |
| Latency | Higher simulated latency | Lower simulated latency |
| Token usage | Higher simulated input/output tokens | Lower simulated tokens |
| Cost | Higher | Lower |
| Failure rate | 1 of 6 | 0 of 6 |

Risk note: do not approve a migration only because the newer configuration is
faster or appears more capable. It must pass the fixed evaluation set and keep
forbidden claims out of the output.

