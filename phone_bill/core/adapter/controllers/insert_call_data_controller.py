from sqlalchemy.orm import Session

from phone_bill.core.adapter.gateways.billing_gateway import BillingGateway
from phone_bill.core.adapter.gateways.call_gateway import CallGateway
from phone_bill.core.dto.call_dto import CallDTO
from phone_bill.core.dto.call_input_dto import CallInputDTO, CallInputType
from phone_bill.core.use_cases.calculate_call_price import CalculateCallPrice
from phone_bill.core.use_cases.handle_end_call_record import HandleEndCallRecord
from phone_bill.core.use_cases.handle_start_call_record import HandleStartCallRecord


class InsertCallDataController:

    def __init__(
        self,
        db: Session,
        call_gateway: CallGateway,
        billing_gateway: BillingGateway,
        start_record_use_case: HandleStartCallRecord,
        end_record_use_case: HandleEndCallRecord,
        calculate_call_price_use_case: CalculateCallPrice,
    ):
        self.call_gateway = call_gateway
        self.billing_gateway = billing_gateway
        self.start_record_use_case = start_record_use_case
        self.end_record_use_case = end_record_use_case
        self.calculate_call_price_use_case = calculate_call_price_use_case
        self.db = db

    def execute(self, data: CallInputDTO):

        if data.type == CallInputType.start:
            call = self.start_record_use_case.execute(self.db, self.call_gateway, data)

        elif data.type == CallInputType.end:
            call = self.end_record_use_case.execute(self.db, self.call_gateway, data)

        if (call.start_timestamp and call.end_timestamp) and not call.price:
            call = self.calculate_call_price_use_case.execute(
                self.db, self.call_gateway, self.billing_gateway, call
            )

        adapter = CallDTO.from_entity(call)

        return adapter
