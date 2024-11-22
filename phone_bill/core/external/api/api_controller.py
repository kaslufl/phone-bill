from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from phone_bill.core.adapter.controllers import InsertCallDataController
from phone_bill.core.adapter.gateways.billing_gateway import BillingGateway
from phone_bill.core.adapter.gateways.call_gateway import CallGateway
from phone_bill.core.dto.call_dto import CallDTO
from phone_bill.core.dto.call_input_dto import CallInputDTO
from phone_bill.core.external.repository.billing_repository import BillingRepository
from phone_bill.core.external.repository.call_repository import CallRepository
from phone_bill.core.use_cases import (
    CalculateCallPrice,
    HandleEndCallRecord,
    HandleStartCallRecord,
)
from phone_bill.infrastructure.database.database import get_session

Session = Annotated[Session, Depends(get_session)]

router = APIRouter(prefix="/call", tags=["call"])


@router.post("", response_model=CallDTO)
def process_call_data(db: Session, data: CallInputDTO):  # type: ignore
    try:
        controller = InsertCallDataController(
            db,
            CallGateway(CallRepository),
            BillingGateway(BillingRepository),
            HandleStartCallRecord,
            HandleEndCallRecord,
            CalculateCallPrice,
        )
        result = controller.execute(data)

        return result
    except Exception as e:
        print(e)
