# steps/shipping.py
from __future__ import annotations
from uuid import uuid4
from saga.context import SagaContext


class ShippingStep:
    name = "Shipping (create)"

    def __init__(self, fail_on_purpose: bool = False) -> None:
        self.fail_on_purpose = fail_on_purpose

    def do(self, ctx: SagaContext) -> None:
        if self.fail_on_purpose:
            raise RuntimeError("shipping provider error")

        shipment_id = "sh_" + uuid4().hex[:8]
        ctx.set("shipment_created", True)
        ctx.set("shipment_id", shipment_id)
        ctx.logs.append(f"  created shipment {shipment_id}")

    def compensate(self, ctx: SagaContext) -> None:
        if not ctx.get("shipment_created", False):
            ctx.logs.append("  cancel skipped (not created)")
            return

        shipment_id = ctx.get("shipment_id")
        ctx.set("shipment_created", False)
        ctx.logs.append(f"  cancelled shipment {shipment_id}")