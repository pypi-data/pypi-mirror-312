from sympy import symbols, integrate, sympify, lambdify
from sympy.parsing.sympy_parser import parse_expr

def integrate_expression(expression_str, var='x', lower_limit=None, upper_limit=None):
    """
    Integrates a mathematical expression with respect to a variable.
    Can compute both indefinite and definite integrals.

    Parameters:
    - expression_str (str): The mathematical expression as a string.
    - var (str): The variable to integrate with respect to (default is 'x').
    - lower_limit (float, optional): The lower limit of integration.
    - upper_limit (float, optional): The upper limit of integration.

    Returns:
    - integral_expr: The symbolic integral expression (indefinite integral).
    - integral_value (optional): The numerical value of the definite integral.
    """
    try:
        # Define the symbol for the variable
        variable = symbols(var)

        # Parse the expression
        expr = parse_expr(expression_str, evaluate=True)

        # Compute the indefinite integral
        integral_expr = integrate(expr, variable)

        if lower_limit is not None and upper_limit is not None:
            # Compute the definite integral
            integral_value = integral_expr.subs(variable, upper_limit) - integral_expr.subs(variable, lower_limit)
            integral_value = integral_value.evalf()
            return integral_expr, integral_value
        else:
            return integral_expr
    except Exception as e:
        raise ValueError(f"An error occurred while integrating the expression: {e}")