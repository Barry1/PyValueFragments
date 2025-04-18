"""Module with small helpers for mathematical questions."""

from __future__ import annotations

from logging import Logger, getLogger

from .moduletools import moduleexport
from .valuetyping import Callable

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
    a1, a2, a3 = cola
    b1, b2, b3 = colb
    c1, c2, c3 = colc
    return a1 * (b2 * c3 - b3 * c2) - a2 * (b1 * c3 - b3 * c1) + a3 * (b1 * c2 - b2 * c1)


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
    a, b, c = coeffs
    c -= val
    discriminant: float = b**2 - 4 * a * c
    if discriminant < 0:
        raise ValueError("Polynomial has no real roots.")
    sqrt_discriminant: float = discriminant**0.5
    root1: float = (-b - sqrt_discriminant) / (2 * a)
    root2: float = (-b + sqrt_discriminant) / (2 * a)
    return root1, root2


@moduleexport
def easybisect(  # pylint: disable=too-many-arguments
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


@moduleexport
def probneeds_rec(needs: list[int], probs: list[float], avails: None | float = None) -> float:
    """Returns the probability for an available number beein sufficient for bernoulli cases."""
    if len(needs) != len(probs):
        raise ValueError("needs and probs must have the same length")
    if __debug__:
        print(f"{needs=}, {probs=}, {avails=}")
    if not needs:
        return 1
    if avails is None:
        avails = sum(n * p for n, p in zip(needs, probs))
        if __debug__:
            print(f"avails set to expectation value {avails}")
    if len(needs) == 1:
        return 1 if avails >= needs[0] else 1 - probs[0]
    return (
        probs[0] * probneeds_rec(needs=needs[1:], probs=probs[1:], avails=avails - needs[0])
        + (1 - probs[0]) * probneeds_rec(needs=needs[1:], probs=probs[1:], avails=avails)
        if avails >= needs[0]
        else (1 - probs[0]) * probneeds_rec(needs=needs[1:], probs=probs[1:], avails=avails)
    )


@moduleexport
def probneeds(needs: list[int], probs: list[float], avails: None | int = None) -> float:
    """Returns the probability for an available number beein sufficient for bernoulli cases."""
    if len(needs) != len(probs):
        raise ValueError("needs and probs must have the same length")
    if avails is None:
        avails = sum(needs)
        thelogger.debug("avails set to overall need value %i", avails)
    stock: dict[int, float] = {avails: 1}
    for need, prob in zip(needs, probs):
        stocktemp: dict[int, float] = {}
        for stockcount, stockprob in stock.items():
            if stockcount - need >= 0:
                stocktemp[stockcount - need] = (
                    stocktemp.get(stockcount - need, 0) + stockprob * prob
                )
            stocktemp[stockcount] = stocktemp.get(stockcount, 0) + stockprob * (1 - prob)
        stock = stocktemp
    thelogger.debug(stock)
    thelogger.info("%i will be sufficient in %f%% of all cases", avails, sum(stock.values()) * 100)
    return sum(stock.values())
