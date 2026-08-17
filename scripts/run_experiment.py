#!/usr/bin/env python3
"""Run a repeatable Sentinel prompt experiment against an OpenAI-compatible API."""

from __future__ import annotations

import argparse
import json
import time
import urllib.error
import urllib.request
from pathlib import Path


DEFAULT_BASE_URL = "http://127.0.0.1:1234/v1"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8").strip()


def call_model(
    *,
    base_url: str,
    model: str,
    system_prompt: str,
    user_prompt: str,
    temperature: float,
    top_p: float | None,
    frequency_penalty: float | None,
    min_p: float | None,
    timeout: int,
) -> dict:
    body = {
        "model": model,
        "temperature": temperature,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    }
    if top_p is not None:
        body["top_p"] = top_p
    if frequency_penalty is not None:
        body["frequency_penalty"] = frequency_penalty
    if min_p is not None:
        body["min_p"] = min_p
    request = urllib.request.Request(
        f"{base_url.rstrip('/')}/chat/completions",
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    started = time.perf_counter()
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
            ok = True
            error = None
    except (urllib.error.URLError, TimeoutError) as exc:
        payload = None
        ok = False
        error = repr(exc)
    return {
        "ok": ok,
        "latency_seconds": round(time.perf_counter() - started, 3),
        "error": error,
        "response": payload,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--incident", required=True, type=Path)
    parser.add_argument("--prompt", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--model", required=True)
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--temperature", default=0.7, type=float)
    parser.add_argument("--top-p", type=float)
    parser.add_argument("--frequency-penalty", type=float)
    parser.add_argument("--min-p", type=float)
    parser.add_argument("--runs", default=1, type=int)
    parser.add_argument("--timeout", default=120, type=int)
    args = parser.parse_args()

    incident = read_text(args.incident)
    prompt = read_text(args.prompt)
    system_prompt = (
        "You are Sentinel, a learning incident-analysis assistant. "
        "Separate supplied facts from assumptions and hypotheses. "
        "Do not claim a confirmed root cause without sufficient evidence. "
        "Do not recommend irreversible production actions."
    )
    user_prompt = f"{prompt}\n\nIncident:\n{incident}"

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("a", encoding="utf-8") as handle:
        for run_index in range(1, args.runs + 1):
            result = call_model(
                base_url=args.base_url,
                model=args.model,
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                temperature=args.temperature,
                top_p=args.top_p,
                frequency_penalty=args.frequency_penalty,
                min_p=args.min_p,
                timeout=args.timeout,
            )
            record = {
                "run_index": run_index,
                "model": args.model,
                "temperature": args.temperature,
                "top_p": args.top_p,
                "frequency_penalty": args.frequency_penalty,
                "min_p": args.min_p,
                "base_url": args.base_url,
                "incident_path": str(args.incident),
                "prompt_path": str(args.prompt),
                **result,
            }
            handle.write(json.dumps(record, ensure_ascii=True) + "\n")
            print(json.dumps(record, ensure_ascii=True))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
