from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from phone_bill.core.external.schema import CallORM


class CallDTO(BaseModel):
    id: int
    start_timestamp: Optional[datetime]
    end_timestamp: Optional[datetime]
    source: Optional[str]
    destination: Optional[str]
    price: Optional[int]

    @classmethod
    def from_orm(cls, data: CallORM):
        return cls(**{**data.__dict__})
