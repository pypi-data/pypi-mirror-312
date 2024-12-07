"""Type aliases for JAX API utilities."""

try:
    import fastapi as _

    from jax.apiutils.fastapi.types import *
except ImportError:
    pass
