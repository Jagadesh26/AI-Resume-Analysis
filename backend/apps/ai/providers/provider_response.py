from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class AIProviderResponse:
    provider: str
    model: str
    raw_text: str
    usage: dict[str, Any] | None = None