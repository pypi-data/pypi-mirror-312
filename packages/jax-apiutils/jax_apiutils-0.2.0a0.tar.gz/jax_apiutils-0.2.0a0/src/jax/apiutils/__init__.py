"""JAX API Utility Package."""

from importlib import metadata

__version__ = metadata.version("jax-apiutils")

try:
    import fastapi as _

    from jax.apiutils.fastapi import *

    try:
        import pydantic as _

        from jax.apiutils.schemas.pydantic import *
    except ImportError:
        pass

except ImportError:
    pass
