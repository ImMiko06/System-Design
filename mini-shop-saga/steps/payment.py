# steps/payment.py
from __future__ import annotations
from saga.context import SagaContext
from store import Store


class PaymentStep:
    name = "Payment (charge)"

    def __init__(self, store: Store) -> None:
        self.store = store

    def do(self, ctx: SagaContext) -> None:
        total: float = ctx.get("total_price")
        if self.store.wallet["balance"] < total:
            raise RuntimeError("insufficient funds")

        self.store.wallet["balance"] -= total
        ctx.set("payment_charged", True)
        ctx.logs.append(f"  charged {total}$")

    def compensate(self, ctx: SagaContext) -> None:
        if not ctx.get("payment_charged", False):
            ctx.logs.append("  refund skipped (not charged)")
            return

        total: float = ctx.get("total_price")
        self.store.wallet["balance"] += total

        ctx.set("payment_charged", False)
        ctx.logs.append(f"  refunded {total}$")