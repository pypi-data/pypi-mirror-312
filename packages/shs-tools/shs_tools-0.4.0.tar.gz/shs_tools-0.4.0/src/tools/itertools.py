from math import factorial, comb
from typing import Sized, Iterator


def len_combinations(iterable: Sized, r: int) -> int:
    """How many options will itertools.combinations(iterable, r) yield?"""
    n = len(iterable)
    if r > n:
        return 0
    else:
        return factorial(n) // factorial(r) // factorial(n - r)


def len_permutations(iterable: Sized, r: int) -> int:
    """How many options will itertools.permutations(iterable, r) yield?"""
    n = len(iterable)
    if r > n:
        return 0
    else:
        return factorial(n) // factorial(n - r)


def combinations_of_sum(total_sum: int, length: int = None, min_value: int = 0) -> Iterator[tuple[int]]:
    if length is None:
        length = total_sum

    if length == 1:
        yield (total_sum,)
    else:
        for value in range(min_value, total_sum + 1):
            for permutation in combinations_of_sum(total_sum - value, length - 1, min_value):
                yield (value,) + permutation


def len_combinations_of_sum(total_sum: int, length: int = None, min_value: int = 0) -> int:
    """
    How many options will combinations_of_sum(total_sum, length) yield?

    No idea how to factor in min_value, yet, so if using min_value, the answer will always be too high
    """
    return comb(total_sum + length - 1, total_sum)
