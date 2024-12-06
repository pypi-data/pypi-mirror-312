# stdmath/ode.py

def derivative(f, x, h=1e-5):
    """Compute the derivative of function f at point x."""
    return (f(x + h) - f(x)) / h