# Sentinel Learning Programme

This repository contains the weekly work for the Sentinel learning programme.

Sentinel is a fictional AI assistant that supports engineers during production
incidents. It is a learning project only: it must not replace an incident
commander and must not independently make or execute production decisions.

## Repository Structure

- `week-1/` - A convincing AI answer can still be unsafe.
- `scripts/` - Small local utilities for running repeatable experiments.
- `outputs/` - Generated model outputs and run logs. Raw outputs are ignored by
  Git by default.

## Week 1 Status

The Week 1 workflow, prompts, evaluation rubric, notes, and local runner are set
up. The remaining required input is the full text of `INC-104 -- Checkout
failures after a deployment`; the course brief links to a Notion page that is
not readable from this environment.

Once the incident text is pasted into `week-1/incidents/INC-104.md`, run at
least five baseline experiments and fill in the evidence tables.

## Local Model Setup

LM Studio is recommended by the course. Start an OpenAI-compatible local server
in LM Studio, then run:

```bash
python3 scripts/run_experiment.py \
  --incident week-1/incidents/INC-104.md \
  --prompt week-1/prompts/baseline.md \
  --model qwen2.5-7b-instruct-1m \
  --output outputs/baseline.jsonl
```

By default the runner calls `http://127.0.0.1:1234/v1/chat/completions`.
