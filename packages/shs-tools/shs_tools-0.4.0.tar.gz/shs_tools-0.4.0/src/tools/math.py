from __future__ import annotations
import math
from decimal import Decimal, ROUND_HALF_UP
from typing import Iterable


def round_half_up(number: int | float) -> int:
    """pythons round() rounds .5 to the *even* number; 0.5 == 0"""
    return int(Decimal(number).to_integral(ROUND_HALF_UP))


def get_factors(num: int) -> set:
    f = {num}
    for x in range(1, int(math.sqrt(num)) + 1):
        if num % x == 0:
            f.add(x)
            f.add(num // x)

    return f


def mul(ints: Iterable[int]) -> int:
    """similar to sum(), just for multiplication"""
    ret = 1
    for x in ints:
        ret *= x

    return ret
