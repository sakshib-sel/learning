# Week 2 Submission

## Application

- Working Claude API application: `src/sentinel_claude/`
- CLI command: `sentinel-claude`
- Structured-output schema: `schemas/sentinel-analysis.schema.json`
- Validator examples: `week-2/examples/`

## Required Exercises

| Exercise | Location |
| --- | --- |
| Streaming and non-streaming examples | `week-2/experiments/streaming.md` |
| Interrupted stream rejection | `week-2/experiments/streaming.md` |
| Valid and invalid structured response | `week-2/examples/` |
| Fictional dashboard image flow | `week-2/experiments/multimodal.md` |
| Typed failure categories | `src/sentinel_claude/failures.py` |
| Direct vs thinking comparison | `week-2/experiments/model-thinking.md` |
| Tokens, latency, stop reason, cost | `week-2/experiments/tokens-cost.md` |
| Prompt caching | `week-2/experiments/prompt-caching.md` |
| Claude Code config | `CLAUDE.md`, `.claude/settings.json` |
| Reusable Claude Code command | `.claude/commands/week2-check.md` |
| Tool-use lifecycle notes | `week-2/experiments/tool-use.md` |
| Debugging report | `week-2/debugging-report.md` |
| Knowledge-check result | `week-2/knowledge-check.md` |

## Live API Status

`ANTHROPIC_API_KEY` was added locally in `.env` and authenticated successfully
against the Anthropic models endpoint. A live Claude generation request failed
because the Anthropic account has insufficient credits. The application handles
this as a typed configuration failure and is ready to run once credits are
available.

## Repository

https://github.com/sakshib-sel/learning
