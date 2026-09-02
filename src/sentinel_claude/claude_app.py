from __future__ import annotations

import base64
import json
import mimetypes
import os
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .failures import FailureCategory, SentinelFailure
from .schema import ANALYSIS_SCHEMA, validate_analysis


SYSTEM_CONTRACT = """You are Sentinel, a learning incident-analysis assistant.
Separate supplied facts from assumptions and hypotheses.
Do not claim a confirmed root cause without sufficient evidence.
Do not recommend irreversible production actions.
Return only JSON that matches the requested incident-analysis contract."""


USER_TASK = """Analyse the incident. Include:
- facts
- assumptions
- hypotheses with supporting evidence, contradicting evidence, and evidence needed
- missing information
- reversible next actions
- uncertainty"""


MODEL_PRICING_PER_MTOK = {
    "claude-sonnet-5": {"input": 2.0, "output": 10.0},
    "claude-sonnet-4-6": {"input": 3.0, "output": 15.0},
    "claude-haiku-4-5": {"input": 1.0, "output": 5.0},
}


@dataclass
class RunMetadata:
    model: str
    mode: str
    latency_seconds: float
    stop_reason: str | None
    input_tokens: int | None
    output_tokens: int | None
    cache_creation_input_tokens: int | None
    cache_read_input_tokens: int | None
    estimated_cost_usd: float | None


def build_messages(incident_text: str, image_path: Path | None = None) -> list[dict[str, Any]]:
    content: list[dict[str, Any]] = [{"type": "text", "text": f"{USER_TASK}\n\nIncident:\n{incident_text}"}]
    if image_path:
        media_type, encoded = encode_image(image_path)
        content.append(
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": media_type,
                    "data": encoded,
                },
            }
        )
    return [{"role": "user", "content": content}]


def encode_image(path: Path) -> tuple[str, str]:
    if not path.exists():
        raise ValueError(f"image does not exist: {path}")
    media_type = mimetypes.guess_type(path.name)[0]
    if media_type not in {"image/png", "image/jpeg", "image/gif", "image/webp"}:
        raise ValueError("image must be png, jpeg, gif, or webp")
    return media_type, base64.b64encode(path.read_bytes()).decode("ascii")


def analyze_incident(
    *,
    incident_path: Path,
    image_path: Path | None,
    model: str,
    max_tokens: int,
    stream: bool,
    thinking_budget_tokens: int | None,
    simulate_interrupt: bool,
) -> dict[str, Any]:
    if not incident_path.exists():
        return _failure(FailureCategory.INPUT, "incident_missing", f"{incident_path} does not exist")
    incident_text = incident_path.read_text(encoding="utf-8").strip()
    if not incident_text:
        return _failure(FailureCategory.INPUT, "incident_empty", "incident text is empty")

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return _failure(
            FailureCategory.CONFIGURATION,
            "missing_api_key",
            "ANTHROPIC_API_KEY is not set",
        )

    try:
        from anthropic import Anthropic
        from anthropic import APIConnectionError, APIStatusError, AuthenticationError, RateLimitError
    except ImportError as exc:
        return _failure(FailureCategory.CONFIGURATION, "sdk_missing", str(exc))

    client = Anthropic(api_key=api_key)
    messages = build_messages(incident_text, image_path)
    request: dict[str, Any] = {
        "model": model,
        "max_tokens": max_tokens,
        "system": [{"type": "text", "text": SYSTEM_CONTRACT, "cache_control": {"type": "ephemeral"}}],
        "messages": messages,
        "output_config": {
            "format": {
                "type": "json_schema",
                "name": "sentinel_incident_analysis",
                "schema": ANALYSIS_SCHEMA,
            }
        },
    }
    if thinking_budget_tokens:
        request["thinking"] = {"type": "enabled", "budget_tokens": thinking_budget_tokens}

    started = time.perf_counter()
    try:
        if stream:
            return _stream_response(
                client=client,
                request=request,
                model=model,
                started=started,
                simulate_interrupt=simulate_interrupt,
            )
        message = client.messages.create(**request)
        text = _message_text(message)
        return _accepted_or_failure(
            text=text,
            metadata=_metadata(message, model, "complete", started),
            raw_response=message.to_dict() if hasattr(message, "to_dict") else None,
        )
    except AuthenticationError as exc:
        return _failure(FailureCategory.CONFIGURATION, "authentication_error", str(exc))
    except RateLimitError as exc:
        return _failure(FailureCategory.INTEGRATION, "rate_limit", str(exc))
    except APIConnectionError as exc:
        return _failure(FailureCategory.INTEGRATION, "connection_error", str(exc))
    except APIStatusError as exc:
        message = str(exc)
        if "credit balance is too low" in message.lower():
            return _failure(
                FailureCategory.CONFIGURATION,
                "insufficient_credits",
                message,
                {"status_code": exc.status_code},
            )
        code = "context_limit" if getattr(exc, "status_code", None) == 400 else "api_status_error"
        return _failure(FailureCategory.INTEGRATION, code, message, {"status_code": exc.status_code})
    except TimeoutError as exc:
        return _failure(FailureCategory.RUNTIME, "timeout", str(exc))


def _stream_response(
    *,
    client: Any,
    request: dict[str, Any],
    model: str,
    started: float,
    simulate_interrupt: bool,
) -> dict[str, Any]:
    chunks: list[str] = []
    try:
        with client.messages.stream(**request) as stream:
            for index, text in enumerate(stream.text_stream):
                chunks.append(text)
                if simulate_interrupt and index >= 0:
                    return _failure(
                        FailureCategory.RUNTIME,
                        "interrupted_stream",
                        "stream interrupted before final message; partial content rejected",
                        {"partial_content": "".join(chunks)},
                    )
            message = stream.get_final_message()
    except KeyboardInterrupt:
        return _failure(
            FailureCategory.RUNTIME,
            "interrupted_stream",
            "stream interrupted before final message; partial content rejected",
            {"partial_content": "".join(chunks)},
        )
    text = _message_text(message)
    return _accepted_or_failure(
        text=text,
        metadata=_metadata(message, model, "stream", started),
        raw_response=message.to_dict() if hasattr(message, "to_dict") else None,
    )


def _accepted_or_failure(
    *,
    text: str,
    metadata: RunMetadata,
    raw_response: dict[str, Any] | None,
) -> dict[str, Any]:
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError as exc:
        return _failure(FailureCategory.MODEL_OUTPUT, "malformed_response", str(exc), {"text": text})

    schema_errors = validate_analysis(parsed)
    if schema_errors:
        return _failure(
            FailureCategory.MODEL_OUTPUT,
            "schema_invalid_output",
            "model output did not match Sentinel analysis schema",
            {"errors": schema_errors, "parsed": parsed},
        )

    return {
        "status": "accepted",
        "analysis": parsed,
        "metadata": asdict(metadata),
        "raw_response": raw_response,
    }


def _message_text(message: Any) -> str:
    parts = []
    for block in getattr(message, "content", []):
        if getattr(block, "type", None) == "text":
            parts.append(getattr(block, "text", ""))
    return "".join(parts).strip()


def _metadata(message: Any, model: str, mode: str, started: float) -> RunMetadata:
    usage = getattr(message, "usage", None)
    input_tokens = getattr(usage, "input_tokens", None)
    output_tokens = getattr(usage, "output_tokens", None)
    cache_creation = getattr(usage, "cache_creation_input_tokens", None)
    cache_read = getattr(usage, "cache_read_input_tokens", None)
    return RunMetadata(
        model=model,
        mode=mode,
        latency_seconds=round(time.perf_counter() - started, 3),
        stop_reason=getattr(message, "stop_reason", None),
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        cache_creation_input_tokens=cache_creation,
        cache_read_input_tokens=cache_read,
        estimated_cost_usd=estimate_cost(model, input_tokens, output_tokens),
    )


def estimate_cost(model: str, input_tokens: int | None, output_tokens: int | None) -> float | None:
    if input_tokens is None or output_tokens is None:
        return None
    prices = MODEL_PRICING_PER_MTOK.get(model)
    if prices is None:
        return None
    return round((input_tokens / 1_000_000 * prices["input"]) + (output_tokens / 1_000_000 * prices["output"]), 6)


def _failure(
    category: FailureCategory,
    code: str,
    message: str,
    details: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {"status": "failure", "failure": SentinelFailure(category, code, message, details).to_dict()}
