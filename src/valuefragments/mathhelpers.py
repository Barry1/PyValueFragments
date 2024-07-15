"""Module with small helpers for mathematical questions."""

from typing import Callable, TypeVar

Tparam = TypeVar("Tparam")


def polyroot(coeffs: tuple[Tparam, Tparam, Tparam], val: Tparam = 0) -> Tparam:
    """Returns root of second order polynom given in its coefficients."""
    val1: Tparam = ((coeffs[1] ** 2 - 4 * coeffs[0] * (coeffs[2] - val)) / 4 / coeffs[0] ** 2) ** (
        1 / 2
    )
    val2: Tparam = coeffs[1] / 2 / coeffs[0]
    return (-val1 - val2, val1 - val2)
