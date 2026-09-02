# Claude Code Instructions

## Purpose

Sentinel is a learning project for AI-assisted production incident analysis. It
helps organize evidence, separate facts from assumptions, generate hypotheses,
and identify missing information.

Sentinel must not replace the incident commander and must not independently
approve or execute production actions.

## Project Structure

- `week-1/` contains prompt experiments, preserved responses, and reflection.
- `week-2/` contains the Claude API application exercises and notes.
- `src/sentinel_claude/` contains the Week 2 Python application.
- `schemas/` contains structured-output contracts.
- `outputs/` may contain generated run artifacts.

## Build And Test

```bash
python3 -m pip install -e .
python3 -m unittest discover -s tests
sentinel-claude validate-json week-2/examples/valid-analysis.json
```

Run a Claude request only when `ANTHROPIC_API_KEY` is configured:

```bash
sentinel-claude analyze --incident week-1/incidents/INC-104.md --model claude-sonnet-5
```

## Coding Conventions

- Keep examples small and readable.
- Keep incident facts separate from model inferences.
- Do not commit API keys or `.env` files.
- Preserve original model outputs without rewriting them.
- Prefer typed failure records over ambiguous exceptions in user-facing output.

## Safety Boundaries

- No production system calls.
- No automatic rollback or operational action.
- No confirmed root-cause claim unless the supplied evidence establishes it.
- Tool requests from Claude are requests only; application code validates and
  controls execution.

## Definition Of Done

- The app accepts validated input or returns a typed failure.
- JSON output is parsed and checked against the Sentinel contract.
- Partial streamed output is rejected.
- Tokens, latency, stop reason, and estimated cost are recorded when available.
- Unsupported API features are documented rather than guessed.

`CLAUDE.md` guides Claude Code behavior, but it is not a security boundary.
Application validation and human review remain required.

