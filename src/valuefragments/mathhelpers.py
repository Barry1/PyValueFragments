"""Module with small helpers for mathematical questions."""

from __future__ import annotations

from logging import Logger, getLogger

from .moduletools import moduleexport
from .valuetyping import Callable

thelogger: Logger = getLogger(__name__)
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
def intp(x_values: Tfloatthreevec, y_values: Tfloatthreevec) -> Tfloatthreevec:
    """Returns coefficients for interpolation by second order polynom along three given pairs."""
    xpowtwo: Tfloatthreevec = (x_values[0] ** 2, x_values[1] ** 2, x_values[2] ** 2)
    majordeterminant: float = determinant(xpowtwo, x_values, (1, 1, 1))
    return (
        determinant(y_values, x_values, (1, 1, 1)) / majordeterminant,
        determinant(xpowtwo, y_values, (1, 1, 1)) / majordeterminant,
        determinant(xpowtwo, x_values, y_values) / majordeterminant,
    )


@moduleexport
def polyroot(coeffs: Tfloatthreevec, val: float = 0) -> tuple[float, float]:
    """Returns root of second order polynom given in its coefficients."""
    assert (
        coeffs[1] ** 2 >= 4 * (coeffs[0] - val) * coeffs[2]
    ), "No real roots as discriminant negative."
    val2: float = coeffs[1] / (2 * coeffs[0])
    val1: float = (val2**2 - (coeffs[2] - val) / coeffs[0]) ** (1 / 2)
    return -val1 - val2, val1 - val2


@moduleexport
def easybisect(  # pylint: disable=too-many-arguments, too-many-positional-arguments
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
            "Iteration %i with relative error %6.3f%%",
            actiter,
            candidatediff * 100 / targetval,
        )
    for entry in data:
        thelogger.debug(entry)
    return data[-1]
