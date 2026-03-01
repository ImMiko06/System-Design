# steps/inventory.py
from __future__ import annotations
from saga.context import SagaContext
from store import Store


class InventoryStep:
    name = "Inventory (reserve)"

    def __init__(self, store: Store) -> None:
        self.store = store

    def do(self, ctx: SagaContext) -> None:
        product_id: str = ctx.get("product_id")
        qty: int = ctx.get("qty")
        product = self.store.products.get(product_id)
        if not product:
            raise RuntimeError("product not found")

        available = product["stock"] - product["reserved"]
        if qty > available:
            raise RuntimeError("not enough stock")

        product["reserved"] += qty
        ctx.set("inventory_reserved", True)
        ctx.logs.append(f"  reserved {qty} of {product_id}")

    def compensate(self, ctx: SagaContext) -> None:
        if not ctx.get("inventory_reserved", False):
            ctx.logs.append("  release skipped (not reserved)")
            return

        product_id: str = ctx.get("product_id")
        qty: int = ctx.get("qty")
        product = self.store.products[product_id]
        product["reserved"] = max(0, product["reserved"] - qty)

        ctx.set("inventory_reserved", False)
        ctx.logs.append(f"  released reservation {qty} of {product_id}")