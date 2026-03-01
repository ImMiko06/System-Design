# saga/step.py
from __future__ import annotations
from typing import Protocol
from .context import SagaContext


class SagaStep(Protocol):
    name: str

    def do(self, ctx: SagaContext) -> None: ...
    def compensate(self, ctx: SagaContext) -> None: ...