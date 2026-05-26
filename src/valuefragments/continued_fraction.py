"""Continued fraction methods."""


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
    residuum: float = initialvalue
    while len(result) < maxlen - 1 and residuum != 0:
        _x = int(residuum)
        result.append(_x)
        residuum = 1 / (residuum - _x)
    result.append(round(residuum))
    return result


def continued_fraction_show(initialvalue: float, maxlen: int = 8):
    print(initialvalue, "\t=>", end=" ")
    chainfracresult: list[int] = continued_fraction(initialvalue, maxlen)
    print(chainfracresult, "\t~", end=" ")
    chainvalresult: float = continued_fraction_val(chainfracresult)
    print(chainvalresult, "\t(Residuum=", end=" ")
    print(initialvalue - chainvalresult, ")")


if __name__ == "__main__":
    from math import pi, e, tau

    continued_fraction_show(e, 3)
    continued_fraction_show(pi, 3)
    continued_fraction_show(tau, 3)
