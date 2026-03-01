# store.py
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class Store:
    products: Dict[str, Dict[str, Any]] = field(default_factory=lambda: {
        "p1": {"id": "p1", "name": "Keyboard", "price": 30.0, "stock": 3, "reserved": 0},
        "p2": {"id": "p2", "name": "Mouse", "price": 15.0, "stock": 5, "reserved": 0},
    })
    wallet: Dict[str, Any] = field(default_factory=lambda: {"user_id": "u1", "balance": 60.0})

    def snapshot(self) -> Dict[str, Any]:
        # удобно печатать состояние магазина
        return {
            "wallet": dict(self.wallet),
            "products": {k: dict(v) for k, v in self.products.items()},
        }