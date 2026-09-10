# Week 4 Submission

## Deliverables

| Deliverable | Location |
| --- | --- |
| Fixed Sentinel evaluation set | `week-4/evaluation/cases.json` |
| Rubric and threshold | `week-4/README.md`, `src/sentinel_claude/evaluation.py` |
| Baseline evaluation results | `outputs/week-4/baseline-eval.json` |
| Model-selection table | `week-4/model-selection.md` |
| Model/config comparison | `week-4/model-migration.md`, `week-4/comparison.md` |
| Token and cost worksheet | `week-4/token-cost-worksheet.md` |
| Prompt-caching experiment | `week-4/prompt-caching.md`, `outputs/week-4/cache-hit.json` |
| Cache invalidation result | `outputs/week-4/cache-invalidation.json` |
| Batch-processing example | `week-4/batch-processing.md`, `outputs/week-4/batch-sim.json` |
| Context pruning and compaction | `week-4/context-engineering.md`, `src/sentinel_claude/context_engineering.py` |
| Model migration risk note | `week-4/model-migration.md` |
| Failure trace | `week-4/failure-trace.md` |
| Updated implementation | `src/sentinel_claude/evaluation.py`, `cache_sim.py`, `batch_sim.py`, `context_engineering.py` |
| Knowledge check | `week-4/knowledge-check.md` |

## Live API Status

The Anthropic key authenticated during Week 2, but live generation failed due to
insufficient credits. Week 4 therefore uses deterministic simulations and does
not invent live model responses.

## Decision

The optimized configuration is acceptable only if it passes the fixed evaluation
set with quality score at or above `0.8` and introduces no forbidden claims.

Result: the optimized deterministic simulation passed 6/6 cases with average
quality score `1.00`, compared with baseline 5/6 and average score `0.90`.

## Repository

https://github.com/sakshib-sel/learning
