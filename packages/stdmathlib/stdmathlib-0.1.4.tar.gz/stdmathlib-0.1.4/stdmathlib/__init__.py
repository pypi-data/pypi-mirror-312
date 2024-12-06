# stdmath/__init__.py

from .algebra import solve_linear, quadratic_formula, solve_equation
from .ode import derivative
from .integrals import integrate_expression

__all__ = [
    'solve_linear',
    'quadratic_formula',
    'solve_equation',
    'derivative',
    'solve_equation',
    'integrate_expression',
]