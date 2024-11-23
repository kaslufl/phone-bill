from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from phone_bill.core.entities.call import Call


class CallDTO(BaseModel):
    id: int
    start_timestamp: Optional[datetime]
    end_timestamp: Optional[datetime]
    source: Optional[str]
    destination: Optional[str]
    price: Optional[int]

    @classmethod
    def from_entity(cls, data: Call):
        return cls(**{**data.__dict__})
