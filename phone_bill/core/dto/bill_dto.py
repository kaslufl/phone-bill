from pydantic import BaseModel, Field

date_regex = r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}$"
hour_regex = r"^(?:[01]?[0-9]|2[0-3]):([0-5]?[0-9]):([0-5]?[0-9])$"
duration_regex = r"^(?:[01]?[0-9]|2[0-3])h([0-5]?[0-9])m([0-5]?[0-9])s$"
monetary_regex = r"/^R\$ (\d{1,3}(\.\d{3})*)(,\d{2})$/gm"


class CallRecordDTO(BaseModel):
    destination: int
    start_date: str = Field(..., pattern=date_regex)
    start_hour: str = Field(..., pattern=hour_regex)
    duration: str = Field(..., pattern=duration_regex)
    price: str = Field(..., pattern=monetary_regex)


class BillDTO(BaseModel):
    subscriber: str
    billing_period: str
    calls: list[CallRecordDTO]
