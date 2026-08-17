# Sentinel Learning

This repo contains my Week 1 work for the Sentinel incident-analysis learning
programme.

Sentinel is a fictional AI assistant for production incidents. It can organize
evidence and suggest investigation steps, but it must not replace the incident
commander or take production action.

## Contents

- `week-1/incidents/` - Incident briefs for INC-104, INC-107, and INC-109.
- `week-1/prompts/` - Baseline, zero-shot, one-shot, few-shot, and JSON-output
  prompts.
- `week-1/responses/` - Preserved model responses.
- `week-1/experiments/` - Prompt comparison and generation-parameter notes.
- `week-1/notes/` - Pre-model analysis, claim classification, and reflection.
- `week-1/submission.md` - Final Week 1 submission summary.
- `scripts/run_experiment.py` - Small runner for OpenAI-compatible model APIs.

## Week 1 Focus

The main lesson is that a convincing model answer can still be unsafe. For
INC-104, the deployment is a plausible hypothesis, but the brief also includes
database latency, external payment-provider errors, and credential-history
signals. The repo separates facts, assumptions, hypotheses, unsupported claims,
and missing evidence.

## Running Experiments

### Local LM Studio

Start an OpenAI-compatible server in LM Studio, then run:

```bash
python3 scripts/run_experiment.py \
  --incident week-1/incidents/INC-104.md \
  --prompt week-1/prompts/json-output/zero-shot-json.md \
  --model qwen2.5-7b-instruct-1m \
  --temperature 0.7 \
  --runs 2 \
  --output outputs/zero-shot-json.jsonl
```

Default base URL:

```text
http://127.0.0.1:1234/v1
```

### Hosted OpenAI-Compatible API

Set an API key in your shell:

```bash
export OPENAI_API_KEY="your-key"
```

Then run:

```bash
python3 scripts/run_experiment.py \
  --base-url https://api.openai.com/v1 \
  --api-key-env OPENAI_API_KEY \
  --incident week-1/incidents/INC-104.md \
  --prompt week-1/prompts/json-output/zero-shot-json.md \
  --model gpt-4.1-mini \
  --temperature 0.7 \
  --top-p 1 \
  --frequency-penalty 0 \
  --response-format json_object \
  --runs 2 \
  --output outputs/openai-zero-shot-json.jsonl
```

Change only one generation parameter at a time and record unsupported settings
as `not supported`.

## Submission

Final Week 1 notes are in:

```text
week-1/submission.md
```
