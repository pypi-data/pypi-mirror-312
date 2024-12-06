from sympy import symbols, diff, sympify, lambdify
from sympy.parsing.sympy_parser import parse_expr

def partial_derivative_expression(expression_str, variables, differentiation_vars, eval_points=None):
    """
    Computes the partial derivative of a multivariable function with respect to specified variables.
    Optionally evaluates the derivative at specific points.

    Parameters:
    - expression_str (str): The multivariable function as a string.
    - variables (list of str): List of variable names in the function.
    - differentiation_vars (list of str): List of variables to differentiate with respect to.
    - eval_points (dict, optional): Dictionary of variable values for evaluation.

    Returns:
    - derivative_expr: The symbolic partial derivative expression.
    - derivative_value (optional): The numerical value of the derivative at eval_points.
    """
    try:
        # Define symbols for all variables
        var_symbols = symbols(variables)
        var_dict = dict(zip(variables, var_symbols))

        # Parse the expression
        expr = parse_expr(expression_str, local_dict=var_dict, evaluate=True)

        # Compute the partial derivative
        derivative_expr = expr
        for var in differentiation_vars:
            derivative_expr = diff(derivative_expr, var_dict[var])

        if eval_points is not None:
            # Substitute the evaluation points into the derivative expression
            derivative_value = derivative_expr.subs(eval_points)
            derivative_value = derivative_value.evalf()
            return derivative_expr, derivative_value
        else:
            return derivative_expr
    except Exception as e:
        raise ValueError(f"An error occurred while computing the partial derivative: {e}")