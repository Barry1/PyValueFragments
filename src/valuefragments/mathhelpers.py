"""Module with small helpers for mathematical questions."""

from logging import Logger, getLogger
from typing import Callable

from .decorators import moduleexport

thelogger: Logger = getLogger(__name__)
# <https://stackoverflow.com/a/50928627>
Tfloatthreevec = tuple[float, float, float]


@moduleexport
def determinant(
    cola: Tfloatthreevec,
    colb: Tfloatthreevec,
    colc: Tfloatthreevec,
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
def intp(x: Tfloatthreevec, y: Tfloatthreevec) -> Tfloatthreevec:
    """Returns coefficients for interpolation by second order polynom along three given pairs."""
    d: float = determinant([val**2 for val in x], x, [1, 1, 1])
    return (
        determinant(y, x, [1, 1, 1]) / d,
        determinant([val**2 for val in x], y, [1, 1, 1]) / d,
        determinant([val**2 for val in x], x, y) / d,
    )


@moduleexport
def polyroot(coeffs: Tfloatthreevec, val: float = 0) -> tuple[float, float]:
    """Returns root of second order polynom given in its coefficients."""
    val1: float = ((coeffs[1] ** 2 - 4 * coeffs[0] * (coeffs[2] - val)) / 4 / coeffs[0] ** 2) ** (
        1 / 2
    )
    val2: float = coeffs[1] / (2 * coeffs[0])
    return (-val1 - val2, val1 - val2)


@moduleexport
def easybisect(
    fun: Callable[[float], float],
    lowerbound: float,
    upperbound: float,
    targetval: float,
    maxiter: int = 20,
    relerror: float = 0.01,
) -> tuple[float, float]:
    """Simple Bisection for scalar functions."""
    thelogger.info("easybisect started")
    thelogger.info("Maximum %i iterations for relative error %f", maxiter, relerror)
    data: list[tuple[float, float]] = []
    assert lowerbound < upperbound
    lowind: int = len(data)
    data.append((lowerbound, fun(lowerbound)))
    highind: int = len(data)
    data.append((upperbound, fun(upperbound)))
    for actiter in range(maxiter):
        candidate: float = data[lowind][0] + (targetval - data[lowind][1]) / (
            data[highind][1] - data[lowind][1]
        ) * (data[highind][0] - data[lowind][0])
        candidateval: float = fun(candidate)
        candidatediff: float = candidateval - targetval
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
