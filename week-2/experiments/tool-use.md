# Tool-Use Preview

Claude can request tool use, but the application controls execution.

## Tool Definition

```json
{
  "name": "lookup_runbook",
  "description": "Return a local runbook summary by runbook id.",
  "input_schema": {
    "type": "object",
    "additionalProperties": false,
    "properties": {
      "runbook_id": { "type": "string" }
    },
    "required": ["runbook_id"]
  }
}
```

## Lifecycle

| Step | Responsibility |
| --- | --- |
| Claude returns `tool_use` | Claude requests a tool call with a tool name and JSON input. |
| Application validates | Check known tool name and validate input schema. |
| Application executes | Run only allowed local code. Do not execute production actions. |
| Application returns `tool_result` | Send the validated result back to Claude. |

## Example

Claude request:

```json
{
  "type": "tool_use",
  "id": "toolu_example_001",
  "name": "lookup_runbook",
  "input": { "runbook_id": "checkout-api-rollback" }
}
```

Application result:

```json
{
  "type": "tool_result",
  "tool_use_id": "toolu_example_001",
  "content": "{\"runbook_id\":\"checkout-api-rollback\",\"summary\":\"Rollback requires incident commander approval and verification of rollback target.\",\"safe_to_execute\":false}"
}
```

