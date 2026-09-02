from __future__ import annotations

import argparse
import json
import zlib
from pathlib import Path

from .claude_app import analyze_incident
from .schema import validate_analysis


def main() -> int:
    parser = argparse.ArgumentParser(prog="sentinel-claude")
    subparsers = parser.add_subparsers(dest="command", required=True)

    analyze = subparsers.add_parser("analyze")
    analyze.add_argument("--incident", required=True, type=Path)
    analyze.add_argument("--image", type=Path)
    analyze.add_argument("--model", default="claude-sonnet-5")
    analyze.add_argument("--max-tokens", type=int, default=1200)
    analyze.add_argument("--stream", action="store_true")
    analyze.add_argument("--thinking-budget-tokens", type=int)
    analyze.add_argument("--simulate-interrupt", action="store_true")
    analyze.add_argument("--output", type=Path)

    validate = subparsers.add_parser("validate-json")
    validate.add_argument("path", type=Path)

    dashboard = subparsers.add_parser("make-dashboard")
    dashboard.add_argument("--output", required=True, type=Path)

    args = parser.parse_args()

    if args.command == "analyze":
        result = analyze_incident(
            incident_path=args.incident,
            image_path=args.image,
            model=args.model,
            max_tokens=args.max_tokens,
            stream=args.stream,
            thinking_budget_tokens=args.thinking_budget_tokens,
            simulate_interrupt=args.simulate_interrupt,
        )
        payload = json.dumps(result, indent=2, ensure_ascii=True)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(payload + "\n", encoding="utf-8")
        print(payload)
        return 0 if result["status"] == "accepted" else 1

    if args.command == "validate-json":
        data = json.loads(args.path.read_text(encoding="utf-8"))
        errors = validate_analysis(data)
        print(json.dumps({"valid": not errors, "errors": errors}, indent=2))
        return 0 if not errors else 1

    if args.command == "make-dashboard":
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_bytes(_dashboard_png())
        print(args.output)
        return 0

    return 2


def _dashboard_png() -> bytes:
    width, height = 640, 360
    rows = []
    for y in range(height):
        row = bytearray([0])
        for x in range(width):
            if y < 56:
                rgb = (25, 34, 45)
            elif 82 < y < 125 and 40 < x < 220:
                rgb = (200, 50, 60)
            elif 160 < y < 205 and 40 < x < 220:
                rgb = (245, 175, 45)
            elif 235 < y < 280 and 40 < x < 220:
                rgb = (65, 160, 95)
            elif 95 < y < 295 and 280 < x < 590:
                line = int(250 - (x - 280) * 0.45 + ((x // 25) % 2) * 25)
                rgb = (80, 170, 230) if abs(y - line) < 4 else (236, 240, 244)
            else:
                rgb = (248, 250, 252)
            row.extend(rgb)
        rows.append(bytes(row))
    raw = b"".join(rows)
    return (
        b"\x89PNG\r\n\x1a\n"
        + _chunk(b"IHDR", width.to_bytes(4, "big") + height.to_bytes(4, "big") + b"\x08\x02\x00\x00\x00")
        + _chunk(b"IDAT", zlib.compress(raw, 9))
        + _chunk(b"IEND", b"")
    )


def _chunk(kind: bytes, data: bytes) -> bytes:
    checksum = zlib.crc32(kind + data) & 0xFFFFFFFF
    return len(data).to_bytes(4, "big") + kind + data + checksum.to_bytes(4, "big")


if __name__ == "__main__":
    raise SystemExit(main())

