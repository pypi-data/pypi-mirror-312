
def factorial(n : int) -> int:
    """Calculates the factorial of a non-negative integer.

    Args:
        n: A non-negative integer.

    Returns:
        The factorial of n.

    Raises:
        TypeError: If n is not an integer.
        ValueError: If n is negative.
    """
    if not isinstance(n, int): raise TypeError("Input must be an integer.")
    if n < 0: raise ValueError("Input must be a non-negative integer.")

    s = 1
    for i in range(2, n + 1): s *= i
    return s

def binary_gcd(n1: int, n2: int) -> int:
    """Calculates the greatest common divisor (GCD) of two non-negative integers
    using the binary GCD algorithm.

    Args:
        n1: A non-negative integer.
        n2: A non-negative integer.

    Returns:
        The greatest common divisor of n1 and n2.

    Raises:
        TypeError: If either n1 or n2 is not an integer.
        ValueError: If either n1 or n2 is negative.
    """
    if not (isinstance(n1, int) and isinstance(n2, int)): raise TypeError("Inputs must be integers.")
    if n1 < 0 or n2 < 0: raise ValueError("Inputs must be non-negative integers.")

    if n1 == 0: return n2
    if n2 == 0:  return n1
    sh = 0
    while (n1 | n2) & 1 == 0:
        sh += 1
        n1 >>= 1
        n2 >>= 1
    while n2 != 0:
        while n2 & 1 == 0:
            n2 >>= 1
        if n1 > n2:
            n1, n2 = n2, n1
        n2 -= n1
    return n1 << sh

def is_prime(n: int) -> bool:
    """Checks if a given non-negative integer is a prime number.

    Args:
        n: A non-negative integer.

    Returns:
        True if n is a prime number, False otherwise.

    Raises:
        TypeError: If n is not an integer.
        ValueError: If n is negative.
    """
    if not isinstance(n, int): raise TypeError("Input must be an integer.")
    if n < 0: raise ValueError("Input must be a non-negative integer.")

    if n <= 1: return False
    if n == 2: return True
    if n % 2 == 0: return False
    j = 3
    while j * j <= n:
        if n % j == 0: return False
        j += 2
    return True

def EratosfenSieve(n : int) -> list:
    """Generates a list of prime numbers up to (but not including) a given integer
    using the Sieve of Eratosthenes algorithm.

    Args:
        n: An integer greater than 1. The upper limit (exclusive) for prime number generation.

    Returns:
        A list of prime numbers less than n.

    Raises:
        TypeError: If n is not an integer.
        ValueError: If n is less than or equal to 1.
    """
    if not isinstance(n, int): raise TypeError("Input must be an integer.")
    if n <= 1: raise ValueError("Input must be an integer greater than 1.")
    
    l = list(range(n - 1))
    l[1] = 0
    for i in l:
        if i > 1:
            for j in range(2 * i, len(l), i):
                l[j] = 0
    return [e for e in l if e != 0]
