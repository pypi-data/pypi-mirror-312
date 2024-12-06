# stdmathlib/algebra.py
from sympy import symbols, Eq, solve, sympify

def solve_linear(a, b):
    """Solve a linear equation ax + b = 0."""
    if a == 0:
        raise ValueError("Coefficient 'a' cannot be zero.")
    return -b / a

def quadratic_formula(a, b, c):
    """Solve a quadratic equation ax^2 + bx + c = 0."""
    import math
    discriminant = b**2 - 4*a*c
    if discriminant < 0:
        raise ValueError("No real roots.")
    x1 = (-b + math.sqrt(discriminant)) / (2*a)
    x2 = (-b - math.sqrt(discriminant)) / (2*a)
    return x1, x2

def solve_equation(equation_str, var='x'):
    """
    Solves an equation for the specified variable.

    Parameters:
    - equation_str (str): The equation as a string, e.g., '((x + 4)/2) = 0'.
    - var (str): The variable to solve for (default is 'x').

    Returns:
    - solutions: A list of solutions for the variable.
    """
    # Define the symbol for the variable
    variable = symbols(var)

    # Check if the equation contains an '=' sign
    if '=' in equation_str:
        # Split the equation into left and right parts
        left_str, right_str = equation_str.split('=')
        # Convert strings to SymPy expressions
        left_expr = sympify(left_str)
        right_expr = sympify(right_str)
        # Form the equation
        equation = Eq(left_expr, right_expr)
    else:
        # If no '=', assume the expression equals zero
        expr = sympify(equation_str)
        equation = Eq(expr, 0)

    # Solve the equation
    solutions = solve(equation, variable)

    return solutions