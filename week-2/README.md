# Week 2 -- Claude Application Boundary

Week 2 turns the Week 1 prompt experiment into a Claude-powered application.

Flow:

```text
Incident text or dashboard image
        ↓
Validated application input
        ↓
Claude Messages API
        ↓
Streamed or complete response
        ↓
Structured-output validation
        ↓
Accepted analysis or typed failure
        ↓
Model, prompt, token, latency, and cache metadata
```

## Run

Install locally:

```bash
python3 -m pip install -e .
```

Set a key:

```bash
export ANTHROPIC_API_KEY="your-key"
```

Non-streaming:

```bash
sentinel-claude analyze \
  --incident week-1/incidents/INC-104.md \
  --model claude-sonnet-5 \
  --output outputs/week-2/non-streaming.json
```

Streaming:

```bash
sentinel-claude analyze \
  --incident week-1/incidents/INC-104.md \
  --model claude-sonnet-5 \
  --stream \
  --output outputs/week-2/streaming.json
```

Interrupted stream simulation:

```bash
sentinel-claude analyze \
  --incident week-1/incidents/INC-104.md \
  --model claude-sonnet-5 \
  --stream \
  --simulate-interrupt
```

Create a fictional dashboard image:

```bash
sentinel-claude make-dashboard --output week-2/assets/fictional-dashboard.png
```

Multimodal request:

```bash
sentinel-claude analyze \
  --incident week-1/incidents/INC-104.md \
  --image week-2/assets/fictional-dashboard.png \
  --model claude-sonnet-5 \
  --output outputs/week-2/multimodal.json
```

## Validate JSON

```bash
sentinel-claude validate-json week-2/examples/valid-analysis.json
sentinel-claude validate-json week-2/examples/invalid-analysis.json
```

## Notes

This app uses the official Anthropic Python SDK when installed. API keys are
read from `ANTHROPIC_API_KEY` and must not be committed.

