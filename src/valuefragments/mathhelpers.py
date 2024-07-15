"""Module with small helpers for mathematical questions."""

from typing import Callable, TypeVar

Tparam = TypeVar("Tparam")


def intp(
    x: tuple[Tparam, Tparam, Tparam], y: tuple[Tparam, Tparam, Tparam]
) -> tuple[Tparam, Tparam, Tparam]:
    """Returns coefficients for interpolation by second order polynom along three given pairs."""
    d: Tparam = (
        x[0] ** 2 * x[1]
        + x[1] ** 2 * x[2]
        + x[2] ** 2 * x[0]
        - x[2] ** 2 * x[1]
        - x[1] ** 2 * x[0]
        - x[0] ** 2 * x[2]
    )
    da: Tparam = y[0] * x[1] + y[1] * x[2] + y[2] * x[0] - y[2] * x[1] - y[1] * x[0] - y[0] * x[2]
    db: Tparam = (
        x[0] ** 2 * y[1]
        + x[1] ** 2 * y[2]
        + x[2] ** 2 * y[0]
        - x[2] ** 2 * y[1]
        - x[1] ** 2 * y[0]
        - x[0] ** 2 * y[2]
    )
    dc: Tparam = (
        x[0] ** 2 * x[1] * y[2]
        + x[1] ** 2 * x[2] * y[0]
        + x[2] ** 2 * x[0] * y[1]
        - x[2] ** 2 * x[1] * y[0]
        - x[1] ** 2 * x[0] * y[2]
        - x[0] ** 2 * x[2] * y[1]
    )
    return (da / d, db / d, dc / d)


def polyroot(coeffs: tuple[Tparam, Tparam, Tparam], val: Tparam = 0) -> Tparam:
    """Returns root of second order polynom given in its coefficients."""
    val1: Tparam = ((coeffs[1] ** 2 - 4 * coeffs[0] * (coeffs[2] - val)) / 4 / coeffs[0] ** 2) ** (
        1 / 2
    )
    val2: Tparam = coeffs[1] / 2 / coeffs[0]
    return (-val1 - val2, val1 - val2)
