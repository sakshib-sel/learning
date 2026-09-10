from __future__ import annotations

import argparse
import json
from pathlib import Path

from .evaluation import estimate_sonnet_cost


BATCH_INCIDENTS = [
    {"id": "INC-201", "urgency": "low", "input_tokens": 1500, "output_tokens": 450},
    {"id": "INC-202", "urgency": "low", "input_tokens": 1650, "output_tokens": 520},
    {"id": "INC-203", "urgency": "medium", "input_tokens": 1420, "output_tokens": 480},
    {"id": "INC-204", "urgency": "low", "input_tokens": 2100, "output_tokens": 610},
    {"id": "INC-205", "urgency": "low", "input_tokens": 1750, "output_tokens": 500},
]


def simulate_batch() -> dict:
    realtime_cost = sum(estimate_sonnet_cost(item["input_tokens"], item["output_tokens"]) for item in BATCH_INCIDENTS)
    batch_cost = round(realtime_cost * 0.5, 6)
    return {
        "mode": "deterministic_simulation",
        "incident_count": len(BATCH_INCIDENTS),
        "appropriate_for_batch": True,
        "reason": "The collection is overnight, non-urgent, and can tolerate delayed completion.",
        "realtime_cost_usd": realtime_cost,
        "batch_cost_usd": batch_cost,
        "estimated_savings_usd": round(realtime_cost - batch_cost, 6),
        "incidents": BATCH_INCIDENTS,
        "retry_policy": "Retry failed requests individually; do not block successful batch results.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(prog="sentinel-batch-sim")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    payload = simulate_batch()
    text = json.dumps(payload, indent=2, ensure_ascii=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

