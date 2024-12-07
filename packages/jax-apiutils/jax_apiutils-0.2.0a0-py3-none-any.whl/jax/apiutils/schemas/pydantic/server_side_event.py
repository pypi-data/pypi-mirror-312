"""Schemas for API Responses."""

import json
from datetime import datetime
from typing import Generic, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T")

__all__ = ["ServerSideEvent"]


class ServerSideEventTemplate(BaseModel, Generic[T]):
    """Schema for server side events."""

    data: T
    id: Optional[str] = None
    retry: Optional[int] = None

    def model_dump_event(self) -> str:
        """Dump the model as an event."""
        # Get the current time and format it
        event_time = datetime.now().strftime("%H:%M:%S")

        # Add the 'time' key to the model's data
        event_data = self.data.dict()
        event_data["time"] = event_time

        # Prepare the event name as the Pydantic class name
        event_name = self.data.__class__.__name__

        # Return the formatted SSE string
        return f"event: {event_name}\ndata: {json.dumps(event_data)}\n\n"


class ServerSideEvent(str):
    """Schema for server side events."""

    def __new__(cls, data: T):
        return ServerSideEventTemplate[T](data=data).model_dump_event()
