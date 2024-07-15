"""Module with small helpers for mathematical questions."""

from logging import Logger, getLogger
from typing import Callable, TypeVar

from .decorators import moduleexport

thelogger: Logger = getLogger(__name__)
Tinput = TypeVar("Tinput", int, float)
Toutput = TypeVar("Toutput", bound=float)


def determinant(
    cola: tuple[float, float, float],
    colb: tuple[float, float, float],
    colc: tuple[float, float, float],
) -> float:
    """Returns Determinant of 3x3-Matrix given in ColumnTuples"""
    return (
        cola[0] * colb[1] * colc[2]
        + cola[1] * colb[2] * colc[0]
        + cola[2] * colb[0] * colc[1]
        - cola[2] * colb[1] * colc[0]
        - cola[1] * colb[0] * colc[2]
        - cola[0] * colb[2] * colc[1]
    )


@moduleexport
def intp(
    x: tuple[Tinput, Tinput, Tinput], y: tuple[Tinput, Tinput, Tinput]
) -> tuple[Tinput, Tinput, Tinput]:
    """Returns coefficients for interpolation by second order polynom along three given pairs."""
    d: Tinput = determinant([val**2 for val in x], x, [1, 1, 1])
    da: Tinput = determinant(y, x, [1, 1, 1])
    db: Tinput = determinant([val**2 for val in x], y, [1, 1, 1])
    dc: Tinput = determinant([val**2 for val in x], x, y)
    return (da / d, db / d, dc / d)


@moduleexport
def polyroot(coeffs: tuple[Tinput, Tinput, Tinput], val: Tinput = 0) -> tuple[Tinput, Tinput]:
    """Returns root of second order polynom given in its coefficients."""
    val1: Tinput = ((coeffs[1] ** 2 - 4 * coeffs[0] * (coeffs[2] - val)) / 4 / coeffs[0] ** 2) ** (
        1 / 2
    )
    val2: Tinput = coeffs[1] / (2 * coeffs[0])
    return (-val1 - val2, val1 - val2)


@moduleexport
def easybisect(
    fun: Callable[[Tinput], Toutput],
    lowerbound: Tinput,
    upperbound: Tinput,
    targetval: Toutput,
    maxiter: int = 20,
    relerror: float = 0.01,
) -> tuple[Tinput, Toutput]:
    """Simple Bisection for scalar functions."""
    thelogger.info("easybisect started")
    thelogger.info("Maximum %i iterations for relative error %f", maxiter, relerror)
    data: list[tuple[Tinput, Toutput]] = []
    assert lowerbound < upperbound
    lowind: int = len(data)
    data.append((lowerbound, fun(lowerbound)))
    highind: int = len(data)
    data.append((upperbound, fun(upperbound)))
    for actiter in range(maxiter):
        candidate: Tinput = data[lowind][0] + (targetval - data[lowind][1]) / (
            data[highind][1] - data[lowind][1]
        ) * (data[highind][0] - data[lowind][0])
        candidateval: Toutput = fun(candidate)
        candidatediff: Toutput = candidateval - targetval
        if candidatediff < 0:
            lowind = len(data)
        else:
            highind = len(data)
        data.append((candidate, candidateval))
        if abs(candidatediff) <= relerror * targetval:
            thelogger.info(
                "Early end of loop at iteration %i with relerr %6.3f%%.",
                actiter,
                candidatediff * 100 / targetval,
            )
            break
        thelogger.debug(
            "Iteration %i with relative error %6.3f%%", actiter, candidatediff * 100 / targetval
        )
    for entry in data:
        thelogger.debug(entry)
    return candidate, candidateval
