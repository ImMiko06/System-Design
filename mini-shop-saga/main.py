# main.py
from __future__ import annotations
from saga.context import SagaContext
from saga.orchestrator import SagaOrchestrator
from store import Store
from steps.inventory import InventoryStep
from steps.payment import PaymentStep
from steps.shipping import ShippingStep


def finalize_order(store: Store, ctx: SagaContext) -> None:
    """Если сага успешна — превращаем reservation в 'sold' (stock уменьшаем)."""
    product_id = ctx.get("product_id")
    qty = ctx.get("qty")
    product = store.products[product_id]

    # reserved -> sold
    product["stock"] -= qty
    product["reserved"] -= qty
    ctx.logs.append(f"FINALIZE: decreased stock by {qty} for {product_id}")


def run_checkout(store: Store, product_id: str, qty: int, fail_shipping: bool) -> SagaContext:
    product = store.products.get(product_id)
    if not product:
        raise RuntimeError("product not found")

    total = product["price"] * qty
    ctx = SagaContext(data={"product_id": product_id, "qty": qty, "total_price": total})

    saga = SagaOrchestrator([
        InventoryStep(store),
        PaymentStep(store),
        ShippingStep(fail_on_purpose=fail_shipping),
    ])

    try:
        saga.execute(ctx)
        finalize_order(store, ctx)
    except Exception:
        # rollback already done inside orchestrator
        pass

    return ctx


if __name__ == "__main__":
    store = Store()

    print("=== INITIAL STORE ===")
    print(store.snapshot())

    print("\n=== CASE 1: FAIL SHIPPING (should rollback) ===")
    ctx1 = run_checkout(store, product_id="p1", qty=1, fail_shipping=True)
    print("\n".join(ctx1.logs))
    print("STORE AFTER FAIL:")
    print(store.snapshot())

    print("\n=== CASE 2: SUCCESS ===")
    ctx2 = run_checkout(store, product_id="p1", qty=1, fail_shipping=False)
    print("\n".join(ctx2.logs))
    print("STORE AFTER SUCCESS:")
    print(store.snapshot())