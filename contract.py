from typing import Dict, Optional

from pydantic import BaseModel, validator


class EventContract(BaseModel):
    # common fields
    event_type: str

    # event-specific content
    event_fields: Dict[str, str]

    @validator("event_fields")
    def event_fields__non_empty(cls, v):
        if len(v) < 1:
            raise ValueError("cannot be empty")
        return v


class QueryEventContract(BaseModel):
    # - common fields
    event_type: str
    #  -- time to start searching
    #     str in ISO 8601 format, (e.g., 2008-09-15T15:53:00+05:00)
    time_start: str
    #  -- time to start searching
    #     str in ISO 8601 format, (e.g., 2008-09-15T15:53:00+05:00)
    time_stop: Optional[str]

    #  - event-specific content
    query_params: Dict[str, str]
