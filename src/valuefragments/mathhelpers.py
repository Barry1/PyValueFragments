"""Module with small helpers for mathematical questions."""

from typing import Callable, TypeVar

Tparam = TypeVar("Tparam")

__all__: list[str] = []


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


__all__.append("intp")


def polyroot(coeffs: tuple[Tparam, Tparam, Tparam], val: Tparam = 0) -> Tparam:
    """Returns root of second order polynom given in its coefficients."""
    val1: Tparam = ((coeffs[1] ** 2 - 4 * coeffs[0] * (coeffs[2] - val)) / 4 / coeffs[0] ** 2) ** (
        1 / 2
    )
    val2: Tparam = coeffs[1] / 2 / coeffs[0]
    return (-val1 - val2, val1 - val2)


__all__.append("polyroot")


def easybisect(
    fun: Callable[[Tinput], Toutput],
    lowerbound: Tinput,
    upperbound: Tinput,
    targetval: Toutput,
    maxiter: int = 20,
    relerror: float = 0.01,
) -> Tinput:
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


__all__.append("easybisect")
