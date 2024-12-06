# stdmath/__init__.py

from .algebra import (
    solve_linear,
    quadratic_formula,
    solve_equation
)
from .ode import (
    derivative,
)
from .pde import (
    partial_derivative_expression,
)
from .integrals import (
    integrate_expression,
)
from .graph import (
    plot,
)

__all__ = [
    'solve_linear',
    'quadratic_formula',
    'solve_equation',
    'derivative',
    'solve_equation',
    'integrate_expression',
    'partial_derivative_expression',
    'plot',
]