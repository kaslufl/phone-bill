from sqlalchemy.orm import Session

from phone_bill.core.adapter.gateways.call_gateway import CallGateway
from phone_bill.core.dto.call_input_dto import CallInputDTO
from phone_bill.core.entities.call import Call
from phone_bill.core.external.schema import CallORM


class HandleEndCallRecord:

    def execute(
        db: Session, call_gateway: CallGateway, call_input: CallInputDTO
    ) -> CallORM:

        call: Call = call_gateway.get_call(db, call_input.call_id)

        if not call:
            call = Call(id=call_input.call_id, end_timestamp=call_input.timestamp)
            return call_gateway.insert_call(db, call)

        call.end_timestamp = call_input.timestamp
        return call_gateway.update_call(db, call)
