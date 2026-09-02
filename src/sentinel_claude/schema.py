from __future__ import annotations

from typing import Any


ANALYSIS_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "required": [
        "facts",
        "assumptions",
        "hypotheses",
        "missing_information",
        "reversible_next_actions",
        "uncertainty",
    ],
    "properties": {
        "facts": {"type": "array", "items": {"type": "string"}},
        "assumptions": {"type": "array", "items": {"type": "string"}},
        "hypotheses": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": [
                    "claim",
                    "supporting_evidence",
                    "contradicting_evidence",
                    "evidence_needed",
                ],
                "properties": {
                    "claim": {"type": "string"},
                    "supporting_evidence": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "contradicting_evidence": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "evidence_needed": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                },
            },
        },
        "missing_information": {"type": "array", "items": {"type": "string"}},
        "reversible_next_actions": {"type": "array", "items": {"type": "string"}},
        "uncertainty": {"type": "string"},
    },
}


def validate_analysis(data: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["analysis must be a JSON object"]

    required = ANALYSIS_SCHEMA["required"]
    for key in required:
        if key not in data:
            errors.append(f"missing required key: {key}")

    for key in ("facts", "assumptions", "missing_information", "reversible_next_actions"):
        if key in data and not _is_string_list(data[key]):
            errors.append(f"{key} must be a list of strings")

    if "uncertainty" in data and not isinstance(data["uncertainty"], str):
        errors.append("uncertainty must be a string")

    if "hypotheses" in data:
        if not isinstance(data["hypotheses"], list):
            errors.append("hypotheses must be a list")
        else:
            for index, item in enumerate(data["hypotheses"]):
                if not isinstance(item, dict):
                    errors.append(f"hypotheses[{index}] must be an object")
                    continue
                for key in (
                    "claim",
                    "supporting_evidence",
                    "contradicting_evidence",
                    "evidence_needed",
                ):
                    if key not in item:
                        errors.append(f"hypotheses[{index}] missing key: {key}")
                if "claim" in item and not isinstance(item["claim"], str):
                    errors.append(f"hypotheses[{index}].claim must be a string")
                for key in ("supporting_evidence", "contradicting_evidence", "evidence_needed"):
                    if key in item and not _is_string_list(item[key]):
                        errors.append(f"hypotheses[{index}].{key} must be a list of strings")

    allowed = set(required)
    for key in data:
        if key not in allowed:
            errors.append(f"unexpected key: {key}")

    return errors


def _is_string_list(value: Any) -> bool:
    return isinstance(value, list) and all(isinstance(item, str) for item in value)

