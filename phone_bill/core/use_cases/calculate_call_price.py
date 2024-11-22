from dataclasses import asdict

from sqlalchemy.orm import Session

from phone_bill.core.adapter.gateways.billing_gateway import BillingGateway
from phone_bill.core.adapter.gateways.call_gateway import CallGateway
from phone_bill.core.dto.call_dto import CallDTO
from phone_bill.core.entities.call import Call
from phone_bill.core.external.schema import CallORM


class CalculateCallPrice:

    def execute(
        db: Session,
        call_gateway: CallGateway,
        billing_gateway: BillingGateway,
        call: CallDTO,
    ) -> CallORM:
        billing_periods = billing_gateway.get_billing_periods(db)
        call: Call = Call(**{**asdict(call)})
        call.calculate_price(billing_periods)

        return call_gateway.update_call(db, call)
