from sympy import symbols, diff, sympify, lambdify
from sympy.parsing.sympy_parser import parse_expr
# stdmathlib/ode.py

def derivative(expression_str, var='x', eval_point=None):
    """
    Differentiates a mathematical expression with respect to a variable.
    Optionally evaluates the derivative at a specific point.

    Parameters:
    - expression_str (str): The mathematical expression as a string.
    - var (str): The variable to differentiate with respect to (default is 'x').
    - eval_point (float, optional): The point at which to evaluate the derivative.

    Returns:
    - derivative_expr: The symbolic derivative expression.
    - derivative_value (optional): The numerical value of the derivative at eval_point.
    """
    try:
        # Define the symbol for the variable
        variable = symbols(var)

        # Parse the expression
        expr = parse_expr(expression_str, evaluate=True)

        # Differentiate the expression
        derivative_expr = diff(expr, variable)

        if eval_point is not None:
            # Create a numerical function from the derivative expression
            derivative_func = lambdify(variable, derivative_expr, modules=['numpy'])
            # Evaluate the derivative at the specified point
            derivative_value = derivative_func(eval_point)
            return derivative_expr, derivative_value
        else:
            return derivative_expr
    except Exception as e:
        raise ValueError(f"An error occurred while differentiating the expression: {e}")