# Streaming And Failure Handling

## Non-Streaming Request

Command:

```bash
sentinel-claude analyze --incident week-1/incidents/INC-104.md --model claude-sonnet-5
```

Expected result:

- Accepted structured analysis when Claude returns valid JSON.
- Typed configuration failure when `ANTHROPIC_API_KEY` is missing.

## Streaming Request

Command:

```bash
sentinel-claude analyze --incident week-1/incidents/INC-104.md --model claude-sonnet-5 --stream
```

Expected result:

- Accumulate stream text.
- Accept only after the final message is available.
- Validate the complete JSON response.

## Interrupted Stream

Command:

```bash
sentinel-claude analyze --incident week-1/incidents/INC-104.md --model claude-sonnet-5 --stream --simulate-interrupt
```

Expected result:

```json
{
  "status": "failure",
  "failure": {
    "category": "runtime",
    "code": "interrupted_stream"
  }
}
```

Partial content is not accepted as a complete incident analysis.

