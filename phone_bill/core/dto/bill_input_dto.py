from typing import Optional
from pydantic import BaseModel, Field
from datetime import date


telephone_regex = r"^\d{10,11}$"
date_regex = r"^(0[1-9]|1[0-2])/(19|20)\d{2}$"


class BillInputDTO(BaseModel):
    subscriber: str = Field(..., pattern=telephone_regex)
    billing_period: str = Field(None, pattern=date_regex)
