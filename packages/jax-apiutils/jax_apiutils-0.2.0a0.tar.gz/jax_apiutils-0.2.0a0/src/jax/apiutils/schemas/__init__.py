"""JAX API schemas."""

try:
    import pydantic as _

    from jax.apiutils.schemas.pydantic import *
except ImportError:
    pass

from . import dataclasses as dataclasses
