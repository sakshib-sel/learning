from __future__ import annotations

import argparse
import json
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .tooling import execute_tool_request, record_to_dict, safety_hook


MAX_TOOL_CALLS = 4
MAX_LOOP_SECONDS = 5.0


DEFAULT_SCRIPTED_REQUESTS = [
    {
        "type": "tool_use",
        "id": "toolu_metrics_001",
        "name": "get_service_metrics",
        "input": {
            "service": "checkout-api",
            "metric": "error_rate",
            "start_time": "10:00",
            "end_time": "10:10",
            "max_points": 3,
        },
    },
    {
        "type": "tool_use",
        "id": "toolu_dep_001",
        "name": "get_dependency_health",
        "input": {
            "service": "checkout-api",
            "dependency": "payments-provider",
            "requested_time": "10:04",
        },
    },
    {
        "type": "tool_use",
        "id": "toolu_logs_001",
        "name": "search_logs",
        "input": {
            "service": "checkout-api",
            "start_time": "10:00",
            "end_time": "10:10",
            "query": "payment provider",
            "max_results": 2,
        },
    },
]


@dataclass
class LoopResult:
    status: str
    tool_calls: int
    elapsed_seconds: float
    records: list[dict[str, Any]]
    final_analysis: dict[str, Any]


def run_scripted_investigation(
    *,
    incident_path: Path,
    identity: str = "sentinel-readonly",
    max_tool_calls: int = MAX_TOOL_CALLS,
    max_loop_seconds: float = MAX_LOOP_SECONDS,
    scripted_requests: list[dict[str, Any]] | None = None,
) -> LoopResult:
    started = time.perf_counter()
    if not incident_path.exists():
        return LoopResult(
            "failure",
            0,
            0.0,
            [],
            {"failure": {"category": "input", "code": "incident_missing"}},
        )

    records: list[dict[str, Any]] = []
    requests = scripted_requests or DEFAULT_SCRIPTED_REQUESTS
    for index, request in enumerate(requests, start=1):
        elapsed = time.perf_counter() - started
        if elapsed > max_loop_seconds:
            return _limited("time_limit_exceeded", index - 1, started, records)
        if index > max_tool_calls:
            return _limited("tool_call_limit_exceeded", index - 1, started, records)
        hook = safety_hook(request.get("name", ""))
        if not hook["allowed"]:
            records.append(
                {
                    "requested_action": request,
                    "validation_result": "blocked_by_hook",
                    "authorization_result": "not checked",
                    "execution_result": hook,
                    "final_sentinel_behaviour": "Stop unsafe action and escalate to human.",
                }
            )
            break
        record = execute_tool_request(request, identity=identity)
        records.append(record_to_dict(record))

    return LoopResult(
        "accepted",
        len(records),
        round(time.perf_counter() - started, 3),
        records,
        _final_analysis(records),
    )


def _limited(
    code: str,
    tool_calls: int,
    started: float,
    records: list[dict[str, Any]],
) -> LoopResult:
    return LoopResult(
        "failure",
        tool_calls,
        round(time.perf_counter() - started, 3),
        records,
        {"failure": {"category": "runtime", "code": code}},
    )


def _final_analysis(records: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "facts": [
            "INC-104 reports checkout failures rising from 0.4% to 9%.",
            "dep-1842 completed shortly before the alert.",
        ],
        "tool_supported_observations": [
            "Mock metrics show checkout error rate elevated between 10:04 and 10:08.",
            "Mock dependency health shows payment-provider degradation near 10:04.",
            "Mock logs include payment-provider 503s and a prompt-injection log line.",
        ],
        "hypotheses": [
            "Payment-provider degradation is a stronger hypothesis after tool evidence.",
            "Deployment regression remains possible but is not confirmed.",
            "Database latency remains a possible contributor.",
        ],
        "safety_notes": [
            "Tool output was treated as untrusted evidence.",
            "Prompt-injection text from logs was not executed as an instruction.",
            "No production write tools exist.",
        ],
        "next_action": "Escalate with evidence summary and request human decision before rollback.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(prog="sentinel-tool-loop")
    parser.add_argument("--incident", default="week-1/incidents/INC-104.md", type=Path)
    parser.add_argument("--identity", default="sentinel-readonly")
    parser.add_argument("--max-tool-calls", default=MAX_TOOL_CALLS, type=int)
    parser.add_argument("--max-loop-seconds", default=MAX_LOOP_SECONDS, type=float)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run_scripted_investigation(
        incident_path=args.incident,
        identity=args.identity,
        max_tool_calls=args.max_tool_calls,
        max_loop_seconds=args.max_loop_seconds,
    )
    payload = json.dumps(asdict(result), indent=2, ensure_ascii=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload + "\n", encoding="utf-8")
    print(payload)
    return 0 if result.status == "accepted" else 1


if __name__ == "__main__":
    raise SystemExit(main())

