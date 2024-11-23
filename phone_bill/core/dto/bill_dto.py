from datetime import date
from pydantic import BaseModel, Field
from babel.numbers import format_currency

from phone_bill.core.external.schema import CallORM

date_regex = r"^(0[1-9]|1[0-2])/(19|20)\d{2}$"
hour_regex = r"^(?:[01]?[0-9]|2[0-3]):([0-5]?[0-9]):([0-5]?[0-9])$"
duration_regex = r"^(?:[01]?[0-9]|2[0-3])h([0-5]?[0-9])m([0-5]?[0-9])s$"
monetary_regex = r"^R\$\s(\d{1,3}(\.\d{3})*)(,\d{2})$"

class CallRecordDTO(BaseModel):
    destination: str
    start_date: str = Field(..., pattern=date_regex)
    start_hour: str = Field(..., pattern=hour_regex)
    duration: str = Field(..., pattern=duration_regex)
    price: str = Field(..., pattern=monetary_regex)
    
    @classmethod
    def from_orm(cls, data: CallORM):
        
        duration = (data.end_timestamp - data.start_timestamp).total_seconds()
        hour = int(duration // 3600)
        minute = int((duration % 3600) // 60)
        seconds = int(duration % 60)
        formated_duration = f"{hour:02}h{minute:02}m{seconds:02}s"
        
        price = data.price / 100

        return cls(
            destination=data.destination,
            start_date=data.start_timestamp.strftime("%m/%Y"),
            start_hour=data.start_timestamp.strftime("%H:%M:%S"),
            duration=formated_duration,
            price=format_currency(price, 'BRL', locale='pt_BR').replace('\xa0', ' '),
        )


class BillDTO(BaseModel):
    subscriber: str
    billing_period: str
    calls: list[CallRecordDTO]
