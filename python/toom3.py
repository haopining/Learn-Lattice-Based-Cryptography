"""
Corrected Toom-3 Multiplication Algorithm
-------------------------------------------

This implementation splits each number into three parts, evaluates the corresponding
polynomials at points [0, 1, -1, 2, ∞], multiplies pointwise, and then fully
interpolates to recover the degree-4 product polynomial.

Multiplication complexities:
- Classical: O(n²)
- Karatsuba: O(n^log₂3) ≈ O(n^1.585)
- Toom-3:    O(n^log₃5) ≈ O(n^1.465)
"""

from typing import Tuple, List
import math


def split_number(n: int, b: int) -> Tuple[int, int, int]:
    """
    Split a number into three parts using base b.
    
    Example:
        >>> split_number(12345, 10)
        (45, 23, 1)  # because 12345 = 45 + 23*10 + 1*100
    """
    x0 = n % b
    x1 = (n // b) % b
    x2 = n // (b * b)
    return x0, x1, x2


def evaluate_at_points(x0: int, x1: int, x2: int) -> List[int]:
    """
    Evaluate the polynomial P(x) = x2*x^2 + x1*x + x0 at points [0, 1, -1, 2, ∞].
    
    Returns:
        List[int]: [P(0), P(1), P(-1), P(2), P(∞)]
    
    Note: P(∞) is taken as the highest-degree coefficient.
    """
    p0 = x0                             # P(0)
    p1 = x0 + x1 + x2                   # P(1)
    p_minus_1 = x0 - x1 + x2            # P(-1)
    p2 = x0 + 2 * x1 + 4 * x2           # P(2)
    p_inf = x2                         # P(∞)
    return [p0, p1, p_minus_1, p2, p_inf]


def interpolate(points: List[int]) -> Tuple[int, int, int, int, int]:
    """
    Interpolate the five coefficients (c0, c1, c2, c3, c4) of the product polynomial
    from the evaluation points.

    Let the product polynomial be:
         C(x) = c0 + c1*x + c2*x^2 + c3*x^3 + c4*x^4

    We have:
         r0 = C(0) = c0
         r1 = C(1) = c0 + c1 + c2 + c3 + c4
         r(-1) = C(-1) = c0 - c1 + c2 - c3 + c4
         r2 = C(2) = c0 + 2c1 + 4c2 + 8c3 + 16c4
         r_inf = C(∞) = c4

    The interpolation is performed as follows:
        c0 = r0
        c4 = r_inf
        c2 = (r1 + r(-1))//2 - c0 - c4
        Let S = (r1 - r(-1))//2 = c1 + c3
        From r2:
           r2 - c0 - 4c2 - 16c4 = 2c1 + 8c3 = 2*(c1 + 4c3)
           But since c1 + c3 = S, we introduce D = c1 - c3.
           It can be shown that:
           D = (5S - (r2 - c0 - 4*c2 - 16*c4)) // 3
        Then:
           c1 = (S + D) // 2
           c3 = (S - D) // 2
    """
    r0, r1, r_minus1, r2, r_inf = points
    c0 = r0
    c4 = r_inf
    # Recover c2
    c2 = (r1 + r_minus1) // 2 - c0 - c4
    # S = c1 + c3
    S = (r1 - r_minus1) // 2
    # From r2:
    temp = r2 - c0 - 4 * c2 - 16 * c4  # equals (2c1 + 8c3)
    # We have 2c1 + 8c3 = 5S - 3D, so:
    D = (5 * S - temp) // 3  # D = c1 - c3
    c1 = (S + D) // 2
    c3 = (S - D) // 2
    return c0, c1, c2, c3, c4


def toom3(x: int, y: int) -> int:
    """
    Multiply two integers using the Toom-3 algorithm.
    
    For small x or y, it falls back to classical multiplication.
    """
    # Base case: for small numbers, use the standard multiplication.
    if x < 1000 or y < 1000:
        return x * y

    # Determine the base for splitting (approximately a cube-root of the number length)
    n = max(len(str(x)), len(str(y)))
    b = 10 ** (n // 3)

    # Split the numbers into three parts.
    x0, x1, x2 = split_number(x, b)
    y0, y1, y2 = split_number(y, b)

    # Evaluate both numbers as polynomials at the five points.
    px = evaluate_at_points(x0, x1, x2)
    py = evaluate_at_points(y0, y1, y2)

    # Pointwise multiplication: multiply the evaluations.
    points = [px[i] * py[i] for i in range(5)]

    # Interpolate to recover the five coefficients.
    c0, c1, c2, c3, c4 = interpolate(points)

    # Recombine the coefficients to get the final product.
    return c0 + c1 * b + c2 * (b ** 2) + c3 * (b ** 3) + c4 * (b ** 4)


def karatsuba(x: int, y: int) -> int:
    """
    A simple implementation of Karatsuba multiplication for comparison.
    """
    # Base case for small numbers
    if x < 10 or y < 10:
        return x * y

    # Calculates the size of the numbers.
    n = max(len(str(x)), len(str(y)))
    half = n // 2

    # Split x and y
    high_x, low_x = divmod(x, 10 ** half)
    high_y, low_y = divmod(y, 10 ** half)

    # 3 recursive calls
    z0 = karatsuba(low_x, low_y)
    z2 = karatsuba(high_x, high_y)
    z1 = karatsuba(low_x + high_x, low_y + high_y) - z2 - z0

    return (z2 * 10 ** (2 * half)) + (z1 * 10 ** half) + z0


def compare_multiplication_methods(x: int, y: int) -> None:
    """
    Compare standard, Karatsuba, and Toom-3 multiplication.
    """
    standard = x * y
    karatsuba_result = karatsuba(x, y)
    toom3_result = toom3(x, y)

    print(f"Numbers: {x} × {y}")
    print(f"Standard:  {standard}")
    print(f"Karatsuba: {karatsuba_result}")
    print(f"Toom-3:    {toom3_result}")
    print(f"All methods agree: {standard == karatsuba_result == toom3_result}\n")


if __name__ == "__main__":
    print("Corrected Toom-3 Multiplication Algorithm Demonstration")
    print("-------------------------------------------------------\n")
    
    # Example 1: Small numbers
    compare_multiplication_methods(123, 456)
    
    # Example 2: Larger numbers
    compare_multiplication_methods(1234567, 7654321)

    # Example 3: Even larger numbers
    a = 12345678901234567890
    b = 98765432109876543210
    compare_multiplication_methods(a, b)


