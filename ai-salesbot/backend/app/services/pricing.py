from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PriceContext:
    base_price: float
    discount_percent_max: float
    wholesale_price: float


def clamp_discount(requested_percent: float, max_percent: float) -> float:
    requested = max(0.0, requested_percent)
    return min(requested, max_percent)