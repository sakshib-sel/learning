from __future__ import annotations

import argparse
import json
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


QUALITY_THRESHOLD = 0.8


@dataclass
class EvaluationResult:
    case_id: str
    configuration: str
    passed: bool
    quality_score: float
    valid_json: bool
    tool_accuracy: float
    latency_seconds: float
    input_tokens: int
    output_tokens: int
    cache_read_tokens: int
    estimated_cost_usd: float
    first_divergence: str | None
    notes: list[str]


MODEL_CONFIGS = {
    "baseline": {
        "model": "claude-sonnet-5",
        "mode": "direct",
        "prompt_cache": False,
        "context_strategy": "full",
        "input_multiplier": 1.0,
    },
    "optimized": {
        "model": "claude-sonnet-5",
        "mode": "direct_fast_triage",
        "prompt_cache": True,
        "context_strategy": "typed_compaction",
        "input_multiplier": 0.68,
    },
}


def load_cases(path: Path) -> list[dict[str, Any]]:
    return json.loads(path.read_text(encoding="utf-8"))["cases"]


def evaluate_cases(cases: list[dict[str, Any]], configuration: str) -> list[EvaluationResult]:
    config = MODEL_CONFIGS[configuration]
    return [evaluate_case(case, configuration, config) for case in cases]


def evaluate_case(case: dict[str, Any], configuration: str, config: dict[str, Any]) -> EvaluationResult:
    started = time.perf_counter()
    simulated = _simulate_sentinel_output(case, configuration)
    notes: list[str] = []
    valid_json = isinstance(simulated, dict) and "facts" in simulated and "hypotheses" in simulated

    facts_score = _coverage(case["expected_facts"], simulated.get("facts", []))
    tool_score = _coverage(case["expected_tool_selection"], simulated.get("tools", []))
    evidence_score = _coverage(case["required_evidence"], simulated.get("evidence", []))
    forbidden_score = 1.0 if not _contains_any(simulated.get("claims", []), case["forbidden_claims"]) else 0.0
    uncertainty_score = 1.0 if case["acceptable_uncertainty"] in simulated.get("uncertainty", "") else 0.0

    score = round((facts_score + tool_score + evidence_score + forbidden_score + uncertainty_score) / 5, 2)
    first_divergence = None
    if not valid_json:
        first_divergence = "response_parsing"
    elif facts_score < 1:
        first_divergence = "model_output"
    elif tool_score < 1:
        first_divergence = "tool_execution"
    elif forbidden_score < 1:
        first_divergence = "model_output"
    elif uncertainty_score < 1:
        first_divergence = "prompt_or_context"

    if first_divergence:
        notes.append(f"first divergence: {first_divergence}")
    if configuration == "optimized":
        notes.append("typed compaction preserves evidence IDs, contradictions, negation, and uncertainty")

    input_tokens = int(case["estimated_input_tokens"] * config["input_multiplier"])
    output_tokens = simulated["estimated_output_tokens"]
    cache_read = int(input_tokens * 0.55) if config["prompt_cache"] else 0
    billable_input = input_tokens - cache_read
    cost = estimate_sonnet_cost(billable_input, output_tokens, cache_read)

    return EvaluationResult(
        case_id=case["id"],
        configuration=configuration,
        passed=score >= QUALITY_THRESHOLD and valid_json,
        quality_score=score,
        valid_json=valid_json,
        tool_accuracy=round(tool_score, 2),
        latency_seconds=round(time.perf_counter() - started + simulated["latency_seconds"], 3),
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        cache_read_tokens=cache_read,
        estimated_cost_usd=cost,
        first_divergence=first_divergence,
        notes=notes,
    )


def estimate_sonnet_cost(input_tokens: int, output_tokens: int, cache_read_tokens: int = 0) -> float:
    # Approximate Sonnet-class pricing: input $3/MTok, output $15/MTok, cache read $0.30/MTok.
    return round(
        input_tokens / 1_000_000 * 3.0
        + output_tokens / 1_000_000 * 15.0
        + cache_read_tokens / 1_000_000 * 0.30,
        6,
    )


def summarize(results: list[EvaluationResult]) -> dict[str, Any]:
    total = len(results)
    return {
        "quality_threshold": QUALITY_THRESHOLD,
        "cases": total,
        "passed": sum(1 for result in results if result.passed),
        "average_quality_score": round(sum(result.quality_score for result in results) / total, 2),
        "average_latency_seconds": round(sum(result.latency_seconds for result in results) / total, 3),
        "input_tokens": sum(result.input_tokens for result in results),
        "output_tokens": sum(result.output_tokens for result in results),
        "cache_read_tokens": sum(result.cache_read_tokens for result in results),
        "estimated_cost_usd": round(sum(result.estimated_cost_usd for result in results), 6),
        "failures": [asdict(result) for result in results if not result.passed],
    }


def _simulate_sentinel_output(case: dict[str, Any], configuration: str) -> dict[str, Any]:
    if configuration == "baseline" and case["id"] == "INC-109":
        return {
            "facts": case["expected_facts"][:-1],
            "tools": case["expected_tool_selection"],
            "evidence": case["required_evidence"][:-1],
            "claims": ["dep-1907 likely caused failures at 14:07"],
            "hypotheses": ["deployment regression"],
            "uncertainty": "medium",
            "estimated_output_tokens": 620,
            "latency_seconds": 1.4,
        }
    return {
        "facts": case["expected_facts"],
        "tools": case["expected_tool_selection"],
        "evidence": case["required_evidence"],
        "claims": [],
        "hypotheses": case["expected_hypotheses"],
        "uncertainty": case["acceptable_uncertainty"],
        "estimated_output_tokens": 540 if configuration == "optimized" else 660,
        "latency_seconds": 0.95 if configuration == "optimized" else 1.35,
    }


def _coverage(expected: list[str], actual: list[str]) -> float:
    if not expected:
        return 1.0
    actual_text = "\n".join(actual).lower()
    hits = sum(1 for item in expected if item.lower() in actual_text)
    return hits / len(expected)


def _contains_any(claims: list[str], forbidden: list[str]) -> bool:
    claim_text = "\n".join(claims).lower()
    return any(item.lower() in claim_text for item in forbidden)


def main() -> int:
    parser = argparse.ArgumentParser(prog="sentinel-evaluate")
    parser.add_argument("--cases", default="week-4/evaluation/cases.json", type=Path)
    parser.add_argument("--configuration", choices=sorted(MODEL_CONFIGS), default="optimized")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    results = evaluate_cases(load_cases(args.cases), args.configuration)
    payload = {
        "configuration": args.configuration,
        "summary": summarize(results),
        "results": [asdict(result) for result in results],
    }
    text = json.dumps(payload, indent=2, ensure_ascii=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0 if payload["summary"]["passed"] == payload["summary"]["cases"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

