"""
Karatsuba Multiplication Algorithm Tutorial
----------------------------------------

The Karatsuba algorithm is a fast multiplication algorithm that was discovered by Anatoly Karatsuba in 1960.
It's more efficient than the classical multiplication algorithm for large numbers.

The main idea is to reduce the number of single-digit multiplications needed for multiplying two n-digit numbers
from n² to approximately n^1.585.

Time Complexity: O(n^log₂3) ≈ O(n^1.585)
Space Complexity: O(n)

Basic principle:
For two numbers x and y with n digits each:
x = a * 10^(n/2) + b
y = c * 10^(n/2) + d
Then: x * y = ac * 10^n + ((a+b)(c+d) - ac - bd) * 10^(n/2) + bd
"""

def karatsuba(x: int, y: int) -> int:
    """
    Multiply two integers using the Karatsuba algorithm.
    
    Args:
        x (int): First number
        y (int): Second number
    
    Returns:
        int: Product of x and y
    
    Example:
        >>> karatsuba(123, 456)
        56088
    """
    # Base case: if numbers are small enough, use standard multiplication
    if x < 10 or y < 10:
        return x * y
    
    # Calculate the number of digits in the larger number
    n = max(len(str(x)), len(str(y)))
    m = n // 2  # Split the number roughly in half
    
    # Split the numbers
    # For example, 1234 with n=4, m=2:
    # a = 12, b = 34
    divisor = 10 ** m
    a = x // divisor  # Left part of x
    b = x % divisor   # Right part of x
    c = y // divisor  # Left part of y
    d = y % divisor   # Right part of y
    
    # Recursive steps
    # Calculate the three products needed
    ac = karatsuba(a, c)    # Multiply left parts
    bd = karatsuba(b, d)    # Multiply right parts
    ad_plus_bc = karatsuba(a + b, c + d) - ac - bd  # Calculate middle term
    
    # Combine the results
    # result = ac * 10^(2*m) + (ad_plus_bc) * 10^m + bd
    return ac * (10 ** (2 * m)) + ad_plus_bc * (10 ** m) + bd


def demonstrate_karatsuba():
    """
    Demonstrate how Karatsuba multiplication works with examples.
    """
    # Example 1: Simple multiplication
    x, y = 123, 456
    result = karatsuba(x, y)
    print(f"Example 1: {x} × {y} = {result}")
    print(f"Verification: {x * y == result}\n")
    
    # Example 2: Larger numbers
    x, y = 12345, 6789
    result = karatsuba(x, y)
    print(f"Example 2: {x} × {y} = {result}")
    print(f"Verification: {x * y == result}\n")
    
    # Example 3: Very large numbers
    x, y = 1234567, 7654321
    result = karatsuba(x, y)
    print(f"Example 3: {x} × {y} = {result}")
    print(f"Verification: {x * y == result}")


if __name__ == "__main__":
    # Run the demonstration
    print("Karatsuba Multiplication Algorithm Demonstration")
    print("----------------------------------------------")
    demonstrate_karatsuba()
    
    # Interactive mode
    print("\nTry it yourself!")
    try:
        x = int(input("Enter first number: "))
        y = int(input("Enter second number: "))
        result = karatsuba(x, y)
        print(f"Result: {x} × {y} = {result}")
        print(f"Verification: {x * y == result}")
    except ValueError:
        print("Please enter valid integers!")