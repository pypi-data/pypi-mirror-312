def factorial(n: int, start: int = 1) -> int:
    """
    n! = 1 * 2 * 3 * 4 * ... * n
    1, 1, 2, 6, 24, 120, 720, ...

    If you're looking for efficiency with start == 1, just use math.factorial(n)
    which takes just 25% of the compute time on average, but this is the fastest
    pure python implementation I could come up with and it allows for partial
    multiplications, like 5 * 6 * 7 * 8 * .... * 17
    """
    if start == n:
        return n
    if n - start == 1:
        return n * start

    middle = start + (n - start) // 2
    return factorial(middle, start) * factorial(n, middle + 1)


def fibonacci(n: int) -> int:
    """
    F(n) = F(n-1) + F(n-2) with F(0) = 0 and F(1) = 1
    0, 1, 1, 2, 3, 5, 8, 13, 21, ...
    """
    if n < 2:
        return n

    l, r = 1, 1
    for _ in range(n - 2):
        l, r = l + r, l

    return l


def triangular(n: int) -> int:
    """
    a(n) = binomial(n+1,2) = n*(n+1)/2 = 0 + 1 + 2 + ... + n
    0, 1, 3, 6, 10, 15, ...
    """
    return n * (n + 1) // 2


def pentagonal(n: int) -> int:
    """
    A pentagonal number is a figurate number that extends the concept of triangular and square numbers to the pentagon
    0, 1, 5, 12, 22, 35, ...
    """
    return ((3 * n * n) - n) // 2


def hexagonal(n: int) -> int:
    if n == 1:
        return 1

    return n * 2 + (n - 1) * 2 + (n - 2) * 2 + hexagonal(n - 1)
