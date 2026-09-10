from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


STABLE_PREFIX = "Sentinel system contract + tool definitions + checkout rollback runbook"


def simulate_cache(change: str | None = None) -> dict:
    prefix = STABLE_PREFIX
    if change == "system_prompt":
        prefix = "Changed Sentinel system contract + tool definitions + checkout rollback runbook"
    if change == "tool_definition":
        prefix = "Sentinel system contract + changed tool definitions + checkout rollback runbook"
    if change == "thinking":
        prefix = "Sentinel system contract + tool definitions + checkout rollback runbook + thinking=enabled"
    digest = hashlib.sha256(prefix.encode("utf-8")).hexdigest()[:12]
    first = {
        "request": "stable prefix + INC-104",
        "cache_key": digest,
        "cache_creation_tokens": 1800,
        "cache_read_tokens": 0,
        "uncached_input_tokens": 650,
        "latency_seconds": 1.4,
        "estimated_cost_usd": 0.00735,
    }
    hit = change is None
    second = {
        "request": "stable prefix + INC-107",
        "cache_key": digest if hit else hashlib.sha256((prefix + change).encode("utf-8")).hexdigest()[:12],
        "cache_creation_tokens": 0 if hit else 1800,
        "cache_read_tokens": 1800 if hit else 0,
        "uncached_input_tokens": 610,
        "latency_seconds": 0.9 if hit else 1.45,
        "estimated_cost_usd": 0.00201 if hit else 0.00723,
    }
    return {
        "mode": "deterministic_simulation",
        "change": change or "none",
        "cache_hit": hit,
        "requests": [first, second],
        "explanation": "Prompt caching reuses a stable prefix; changing content before the checkpoint invalidates the cache.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(prog="sentinel-cache-sim")
    parser.add_argument("--change", choices=["system_prompt", "tool_definition", "thinking"])
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    payload = simulate_cache(args.change)
    text = json.dumps(payload, indent=2, ensure_ascii=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

