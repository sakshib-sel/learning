from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any


class FailureCategory(str, Enum):
    INPUT = "input"
    CONFIGURATION = "configuration"
    INTEGRATION = "integration"
    RUNTIME = "runtime"
    MODEL_OUTPUT = "model_output"


@dataclass
class SentinelFailure:
    category: FailureCategory
    code: str
    message: str
    details: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

