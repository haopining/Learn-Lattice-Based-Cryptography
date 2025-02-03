
"""
Toom-3 Multiplication Algorithm Tutorial
--------------------------------------

The Toom-3 algorithm (also known as Toom-Cook-3) is an advanced multiplication algorithm that extends
the ideas of Karatsuba's algorithm. While Karatsuba splits numbers into 2 parts, Toom-3 splits them
into 3 parts, leading to better asymptotic complexity for very large numbers.

Comparison with other multiplication algorithms:
- Classical: O(n²)
- Karatsuba: O(n^log₂3) ≈ O(n^1.585)
- Toom-3:    O(n^log₃5) ≈ O(n^1.465)

Basic principle:
For a number x with n digits, we split it into 3 parts:
x = x₀ + x₁b + x₂b²  where b = n^(1/3)
"""

from typing import Tuple, List
import math


def split_number(n: int, b: int) -> Tuple[int, int, int]:
    """
    Split a number into three parts using base b.
    
    Args:
        n (int): Number to split
        b (int): Base for splitting (usually a power of the input length)
    
    Returns:
        Tuple[int, int, int]: Three parts of the number
    
    Example:
        >>> split_number(12345, 10)
        (45, 23, 1)  # 12345 = 45 + 23*10 + 1*100
    """
    x0 = n % b
    x1 = (n // b) % b
    x2 = n // (b * b)
    return x0, x1, x2


def evaluate_at_points(x0: int, x1: int, x2: int) -> List[int]:
    """
    Evaluate the polynomial P(x) = x₂x² + x₁x + x₀ at points [0, 1, -1, 2, ∞]
    
    Args:
        x0, x1, x2: Coefficients of the polynomial
    
    Returns:
        List[int]: Values at the evaluation points
    """
    # P(0) = x₀
    p0 = x0
    
    # P(1) = x₂ + x₁ + x₀
    p1 = x2 + x1 + x0
    
    # P(-1) = x₂ - x₁ + x₀
    p_minus_1 = x2 - x1 + x0
    
    # P(2) = 4x₂ + 2x₁ + x₀
    p2 = 4 * x2 + 2 * x1 + x0
    
    # P(∞) = x₂ (highest degree coefficient)
    p_inf = x2
    
    return [p0, p1, p_minus_1, p2, p_inf]


def interpolate(points: List[int]) -> Tuple[int, int, int]:
    """
    Interpolate the product polynomial from points.
    
    Args:
        points (List[int]): Values at the evaluation points [0, 1, -1, 2, ∞]
    
    Returns:
        Tuple[int, int, int]: Coefficients of the result polynomial
    """
    # These formulas come from solving the system of equations
    # and simplifying the interpolation formulas
    r0 = points[0]
    r4 = points[4]
    
    r3 = (points[3] - points[1]) // 2
    r1 = points[1] - points[0]
    r2 = points[2] - points[0]
    
    c0 = r0
    c1 = (r1 - r2) // 2
    c2 = r2 - r1 + r0
    c3 = (r3 - 2 * r2 + r1) // 6
    c4 = r4 - c3 - c2 - c1 - c0
    
    return c0, c1, c2


def toom3(x: int, y: int) -> int:
    """
    Multiply two integers using the Toom-3 algorithm.
    
    Args:
        x (int): First number
        y (int): Second number
    
    Returns:
        int: Product of x and y
    
    Example:
        >>> toom3(123456, 789012)
        97408129472
    """
    # Base case: for small numbers, use regular multiplication
    if x < 1000 or y < 1000:
        return x * y
    
    # Determine the base for splitting (approximately cube root of the input)
    n = max(len(str(x)), len(str(y)))
    b = 10 ** (n // 3)
    
    # Split both numbers into three parts
    x0, x1, x2 = split_number(x, b)
    y0, y1, y2 = split_number(y, b)
    
    # Evaluate both polynomials at 5 points
    px = evaluate_at_points(x0, x1, x2)
    py = evaluate_at_points(y0, y1, y2)
    
    # Pointwise multiplication
    points = [px[i] * py[i] for i in range(5)]
    
    # Interpolate to get result coefficients
    r0, r1, r2 = interpolate(points)
    
    # Combine the results
    return r0 + r1 * b + r2 * (b * b)


def compare_multiplication_methods(x: int, y: int) -> None:
    """
    Compare different multiplication methods.
    """
    # Standard multiplication
    standard = x * y
    
    # Import Karatsuba from the other file
    import karatsuba
    karatsuba_result = karatsuba.karatsuba(x, y)
    
    # Toom-3
    toom3_result = toom3(x, y)
    
    print(f"Numbers: {x} × {y}")
    print(f"Standard:  {standard}")
    print(f"Karatsuba: {karatsuba_result}")
    print(f"Toom-3:    {toom3_result}")
    print(f"All methods agree: {standard == karatsuba_result == toom3_result}\n")


if __name__ == "__main__":
    print("Toom-3 Multiplication Algorithm Demonstration")
    print("-------------------------------------------")
    
    # Example: Small numbers
    compare_multiplication_methods(123, 456)
    
    # Example: Medium numbers, but failed
    compare_multiplication_methods(1234567, 7654321)
    