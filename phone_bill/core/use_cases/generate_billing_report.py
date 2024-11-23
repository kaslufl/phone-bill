from datetime import datetime
from sqlalchemy.orm import Session

from phone_bill.core.adapter.gateways.call_gateway import CallGateway
from phone_bill.core.dto import BillDTO, CallRecordDTO
from phone_bill.core.external.schema import CallORM

class GenerateBillingReport:

    def execute(
        db: Session, call_gateway: CallGateway, subscriber: str, billing_year: int=None, billing_month: int=None
    ) -> BillDTO:

        if billing_year and billing_month:
            period = datetime(month=billing_month, year=billing_year, day=1)
            
        else:
            today = datetime.now()
            period = datetime(today.year, today.month-1, 1) if today.month != 1 else datetime(today.year - 1, 12, 1)

        call_list: list[CallORM] = call_gateway.get_billing(db, subscriber, period)

        formated_calls = [CallRecordDTO.from_orm(call) for call in call_list]

        return BillDTO(subscriber=subscriber, billing_period=period.strftime("%m/%Y"), calls=formated_calls)
