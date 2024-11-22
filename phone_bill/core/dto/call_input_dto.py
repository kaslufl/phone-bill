from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

telephone_regex = r"^\d{10,11}$"


class CallInputType(str, Enum):
    start = "start"
    end = "end"


class CallInputDTO(BaseModel):
    id: int
    type: CallInputType
    timestamp: datetime
    call_id: int
    source: Optional[str] = Field(None, pattern=telephone_regex)
    destination: Optional[str] = Field(None, pattern=telephone_regex)
