"""Continued fraction methods."""

from math import ceil, e, floor, pi, tau


def continued_fraction_val(chain: list[int]) -> float:
    """Returns the value of a continued fraction."""
    result: float = float(chain[-1])
    for x in reversed(chain[:-1]):
        result = x + 1 / result
    return result


# def continued_fraction_val(chain: list[int]) -> float:
#    """Returns the value of a continued fraction."""
#    result: float = 0
#    for x in reversed(chain[1:]):
#        result = 1 / (result + x)
#    return chain[0] + result


def continued_fraction(initialvalue: float, maxlen: int = 8) -> list[int]:
    """Returns the continued fraction representation of a number."""
    result: list[int] = []
    result.append(floor(initialvalue))
    residuum: float = initialvalue - result[-1]
    while len(result) < maxlen - 1 and residuum:
        residuum = 1 / residuum
        result.append(floor(residuum))
        residuum = residuum - result[-1]
    if residuum:
        result.append(round(1 / residuum))
    return result


def continued_fraction_interval(
    initialvalue: float, maxlen: int = 8
) -> list[int | tuple[int, int]]:
    """Returns the continued fraction representation of a number."""
    result: list[int | tuple[int, int]] = []
    residuum: float = initialvalue
    while len(result) < maxlen - 1 and residuum != 0:
        _x = floor(residuum)
        result.append(_x)
        residuum = 1 / (residuum - _x)
    result.append((floor(residuum), ceil(residuum)))
    return result


def continued_fraction_show(initialvalue: float, maxlen: int = 8) -> None:
    print(initialvalue, "\t=>", end=" ")
    chainfracresult: list[int] = continued_fraction(initialvalue, maxlen)
    print(chainfracresult, "\t~", end=" ")
    chainvalresult: float = continued_fraction_val(chainfracresult)
    print(chainvalresult, "\t(Residuum=", end=" ")
    print(initialvalue - chainvalresult, ")")


class ContinuedFraction:
    """Class for continued fraction representation of a number.
    <https://mathworld.wolfram.com/RegularContinuedFraction.html>
    """

    def __init__(self, initialvalue: float, maxlen: int = 8) -> None:
        self.precision: int = maxlen
        self.initialvalue: float = initialvalue
        self.chain: list[int] = continued_fraction(initialvalue, maxlen)
        self.value: float = continued_fraction_val(self.chain)

    @property
    def interval(self) -> list[int | tuple[int, int]]:
        return continued_fraction_interval(self.value, len(self.chain))

    @property
    def residuum(self) -> float:
        return self.initialvalue - self.value


if __name__ == "__main__":
    continued_fraction_show(e, 3)
    print(continued_fraction_interval(e, 3))
    continued_fraction_show(pi, 3)
    print(continued_fraction_interval(pi, 3))
    continued_fraction_show(-pi, 3)
    print(continued_fraction_interval(-pi, 3))
    continued_fraction_show(tau, 3)
    print(continued_fraction_interval(tau, 3))
