"""Exceptions for the JAX APIs."""

try:
    import fastapi as _

    from jax.apiutils.fastapi.exceptions import *
except ImportError:
    pass
