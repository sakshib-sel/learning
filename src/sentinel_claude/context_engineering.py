from __future__ import annotations


CRITICAL_KEYS = {
    "evidence_id",
    "source",
    "finding",
    "negative_finding",
    "contradiction",
    "uncertainty",
    "decision",
}


def prune_tool_results(results: list[dict], max_observations: int = 3) -> list[dict]:
    pruned = []
    for result in results:
        kept = {key: value for key, value in result.items() if key in CRITICAL_KEYS}
        observations = result.get("observations", [])
        if isinstance(observations, list):
            kept["observations"] = observations[:max_observations]
        pruned.append(kept)
    return pruned


def compact_context(results: list[dict]) -> dict:
    return {
        "evidence_ids": [item.get("evidence_id") for item in results if item.get("evidence_id")],
        "negative_findings": [item.get("negative_finding") for item in results if item.get("negative_finding")],
        "contradictions": [item.get("contradiction") for item in results if item.get("contradiction")],
        "unresolved_uncertainty": [item.get("uncertainty") for item in results if item.get("uncertainty")],
        "decisions_already_made": [item.get("decision") for item in results if item.get("decision")],
        "source_attribution": [item.get("source") for item in results if item.get("source")],
    }

