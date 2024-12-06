# stdmathlib/combinatorics.py
from math import factorial as math_factorial

def factorial(n):
    """
    Computes the factorial of n (n!).
    
    Parameters:
    - n (int): The number to compute the factorial of (n >= 0).
    
    Returns:
    - int: The factorial of n.
    """
    if n < 0:
        raise ValueError("n must be a non-negative integer.")
    return math_factorial(n)

def permutations(n, k):
    """
    Computes the number of permutations (nPk).
    
    Parameters:
    - n (int): Total number of items.
    - k (int): Number of items to choose (k <= n).
    
    Returns:
    - int: The number of permutations.
    """
    if n < 0 or k < 0:
        raise ValueError("n and k must be non-negative integers.")
    if k > n:
        return 0
    return math_factorial(n) // math_factorial(n - k)

def combinations(n, k):
    """
    Computes the number of combinations (nCk).
    
    Parameters:
    - n (int): Total number of items.
    - k (int): Number of items to choose (k <= n).
    
    Returns:
    - int: The number of combinations.
    """
    if n < 0 or k < 0:
        raise ValueError("n and k must be non-negative integers.")
    if k > n:
        return 0
    return math_factorial(n) // (math_factorial(k) * math_factorial(n - k))

def pigeonhole_principle(total_items, pigeonholes):
    """
    Computes the minimum number of items required to ensure that at least one pigeonhole
    contains more than one item.
    
    Parameters:
    - total_items (int): Total number of items.
    - pigeonholes (int): Number of pigeonholes.
    
    Returns:
    - int: The minimum number of items to guarantee at least one pigeonhole has more than one item.
    """
    if pigeonholes <= 0:
        raise ValueError("Number of pigeonholes must be a positive integer.")
    return pigeonholes + 1