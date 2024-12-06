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
    
def integrate_multivariable_expression(expression_str, variables, limits=None):
    """
    Computes the multivariable integral of an expression with respect to specified variables.
    Can compute both indefinite and definite integrals.

    Parameters:
    - expression_str (str): The mathematical expression as a string.
    - variables (list of str): List of variable names to integrate with respect to.
    - limits (list of tuples, optional): List of tuples specifying the limits for each variable.
      Each tuple should be (variable_name, lower_limit, upper_limit).

    Returns:
    - For indefinite integrals: The symbolic integral expression.
    - For definite integrals: The numerical value of the definite integral.
    """
    try:
        # Define symbols for all variables
        var_symbols = symbols(variables)
        var_dict = dict(zip(variables, var_symbols))

        # Parse the expression
        expr = parse_expr(expression_str, local_dict=var_dict, evaluate=True)

        # Prepare the integration variables and limits
        if limits is not None:
            # Definite integral
            integration_limits = []
            for var_name, lower_limit, upper_limit in limits:
                var = var_dict[var_name]
                integration_limits.append((var, lower_limit, upper_limit))
            # Compute the definite integral
            integral_result = integrate(expr, *integration_limits)
            integral_value = integral_result.evalf()
            return integral_value
        else:
            # Indefinite integral
            integral_expr = expr
            for var in var_symbols:
                integral_expr = integrate(integral_expr, var)
            return integral_expr
    except Exception as e:
        raise ValueError(f"An error occurred while integrating the expression: {e}")