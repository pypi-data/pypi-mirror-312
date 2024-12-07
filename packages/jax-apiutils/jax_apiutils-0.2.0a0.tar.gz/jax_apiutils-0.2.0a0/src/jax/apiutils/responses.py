"""JAX API responses."""

try:
    import fastapi as _

    from jax.apiutils.fastapi.responses import *
except ImportError:
    pass
