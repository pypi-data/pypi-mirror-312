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
    integrate_multivariable_expression,
)
from .graph import (
    plot,
)
from .combinatorics import (
    factorial, # !
    combinations, # nCr
    permutations, # nPr
    pigeonhole_principle, # pigeon
)

__all__ = [
    'solve_linear',
    'quadratic_formula',
    'solve_equation',
    'derivative',
    'solve_equation',
    'integrate_expression',
    'partial_derivative_expression',
    'integrate_multivariable_expression',
    'factorial',
    'combinations',
    'permutations',
    'pigeonhole_principle',
    'plot',
]