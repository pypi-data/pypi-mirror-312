import matplotlib.pyplot as plt
import numpy as np
from sympy import symbols, lambdify
from sympy.parsing.sympy_parser import parse_expr

def plot(
    expression_str,
    var='x',
    range_start=-10,
    range_end=10,
    num_points=1000,
    title=None,
    xlabel=None,
    ylabel=None,
    line_style='-',
    color='blue'
):
    """
    Plots a mathematical expression using matplotlib.

    Parameters:
    - expression_str (str): The mathematical expression as a string, e.g., 'sin(x)'.
    - var (str): The variable in the expression (default is 'x').
    - range_start (float): The start of the range for the variable (default is -10).
    - range_end (float): The end of the range for the variable (default is 10).
    - num_points (int): The number of points to compute for plotting (default is 1000).
    - title (str): The title of the plot.
    - xlabel (str): The label for the x-axis.
    - ylabel (str): The label for the y-axis.
    - line_style (str): The line style for the plot (default is '-').
    - color (str): The color of the plot line (default is 'blue').

    Returns:
    - None: Displays the plot.
    """
    try:
        # Define the symbol for the variable
        variable = symbols(var)
        local_dict = {var: variable}

        # Parse the expression
        expr = parse_expr(expression_str, local_dict=local_dict, evaluate=True)

        # Convert the symbolic expression to a numerical function
        func = lambdify(variable, expr, modules=['numpy'])

        # Generate the range of values
        x_vals = np.linspace(range_start, range_end, num_points)
        y_vals = func(x_vals)

        # Create the plot
        plt.figure(figsize=(8, 6))
        plt.plot(x_vals, y_vals, line_style, color=color, label=f"y = {expression_str}")

        # Set plot title and labels
        if title is not None:
            plt.title(title)
        else:
            plt.title(f"Plot of {expression_str}")

        if xlabel is not None:
            plt.xlabel(xlabel)
        else:
            plt.xlabel(var)

        if ylabel is not None:
            plt.ylabel(ylabel)
        else:
            plt.ylabel('y')

        plt.grid(True)
        plt.legend()
        plt.show()

    except Exception as e:
        raise ValueError(f"An error occurred while plotting the expression: {e}")