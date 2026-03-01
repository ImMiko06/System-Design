# saga/orchestrator.py
from __future__ import annotations
from typing import List
from .context import SagaContext
from .step import SagaStep


class SagaOrchestrator:
    def __init__(self, steps: List[SagaStep]) -> None:
        self.steps = steps

    def execute(self, ctx: SagaContext) -> None:
        completed: List[SagaStep] = []

        try:
            for step in self.steps:
                ctx.logs.append(f"DO: {step.name}")
                step.do(ctx)
                completed.append(step)

            ctx.logs.append("SAGA SUCCESS ✅")

        except Exception as e:
            ctx.logs.append(f"SAGA FAILED ❌ reason={e}")

            for step in reversed(completed):
                ctx.logs.append(f"COMPENSATE: {step.name}")
                try:
                    step.compensate(ctx)
                except Exception as ce:
                    # в реальности: лог + алерт, компенсации должны быть идемпотентны
                    ctx.logs.append(f"  compensation error in {step.name}: {ce}")

            ctx.logs.append("SAGA ROLLED BACK 🔁")
            raise