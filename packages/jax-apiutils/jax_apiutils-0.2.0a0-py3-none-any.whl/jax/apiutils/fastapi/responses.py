"""Custom FastAPI Responses."""

from typing import AsyncIterable

from fastapi.responses import StreamingResponse

from jax.apiutils.schemas.pydantic.server_side_event import ServerSideEvent


class ServerSideEventResponse(StreamingResponse):
    """Schema for server side event responses."""

    def __init__(self, iterator: AsyncIterable):
        super().__init__(
            content=(ServerSideEvent(data=item) async for item in iterator),
            media_type="text/event-stream",
        )
