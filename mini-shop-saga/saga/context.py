# saga/context.py
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class SagaContext:
    data: Dict[str, Any] = field(default_factory=dict)
    logs: List[str] = field(default_factory=list)

    def set(self, key: str, value: Any) -> None:
        self.data[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)