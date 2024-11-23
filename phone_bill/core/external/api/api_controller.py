from typing import Annotated
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from phone_bill.core.adapter.controllers import (
    InsertCallDataController,
    GenerateReportController,
)
from phone_bill.core.adapter.gateways import (
    BillingGateway,
    CallGateway,
)
from phone_bill.core.dto import (
    BillDTO,
    BillInputDTO,
    CallDTO,
    CallInputDTO,
)
from phone_bill.core.entities.exceptions import InvalidParam
from phone_bill.core.external.repository import (
    BillingRepository,
    CallRepository,
)
from phone_bill.core.use_cases import (
    CalculateCallPrice,
    HandleEndCallRecord,
    HandleStartCallRecord,
    GenerateBillingReport,
)
from phone_bill.infrastructure.database.database import get_session

Session = Annotated[Session, Depends(get_session)]

router = APIRouter(prefix="/call", tags=["call"])


@router.post("", response_model=CallDTO)
def process_call_data(db: Session, data: CallInputDTO):  # type: ignore
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

@router.get('/report', response_model=BillDTO)
def get_report(db: Session, billing_filter: Annotated[BillInputDTO, Query()]):  # type: ignore
    controller = GenerateReportController(
        db,
        CallGateway(CallRepository),
        GenerateBillingReport,
    )
    try:
        result: BillDTO = controller.execute(billing_filter)
        
        if not result.calls:
            raise HTTPException(HTTPStatus.NOT_FOUND, detail='No data was found.')

        return result

    except InvalidParam as e:
        raise HTTPException(HTTPStatus.BAD_REQUEST, detail=e.args[0])
