from __future__ import annotations

import json


TOOL_DEFINITION = {
    "name": "lookup_runbook",
    "description": "Return a local runbook summary by runbook id.",
    "input_schema": {
        "type": "object",
        "additionalProperties": False,
        "properties": {"runbook_id": {"type": "string"}},
        "required": ["runbook_id"],
    },
}


EXAMPLE_TOOL_USE = {
    "type": "tool_use",
    "id": "toolu_example_001",
    "name": "lookup_runbook",
    "input": {"runbook_id": "checkout-api-rollback"},
}


EXAMPLE_TOOL_RESULT = {
    "type": "tool_result",
    "tool_use_id": "toolu_example_001",
    "content": json.dumps(
        {
            "runbook_id": "checkout-api-rollback",
            "summary": "Rollback requires incident commander approval and verification of rollback target.",
            "safe_to_execute": False,
        }
    ),
}


def validate_tool_use(block: dict) -> list[str]:
    errors: list[str] = []
    if block.get("type") != "tool_use":
        errors.append("block type must be tool_use")
    if block.get("name") != TOOL_DEFINITION["name"]:
        errors.append("unknown tool requested")
    tool_input = block.get("input")
    if not isinstance(tool_input, dict):
        errors.append("tool input must be an object")
    elif not isinstance(tool_input.get("runbook_id"), str):
        errors.append("runbook_id must be a string")
    return errors

