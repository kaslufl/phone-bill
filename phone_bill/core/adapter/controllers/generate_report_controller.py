from datetime import datetime
from sqlalchemy.orm import Session

from phone_bill.core.adapter.gateways import CallGateway
from phone_bill.core.use_cases import GenerateBillingReport
from phone_bill.core.dto import BillInputDTO
from phone_bill.core.entities.exceptions import InvalidParam


class GenerateReportController:
    
    def __init__(
        self,
        db: Session,
        call_gateway: CallGateway,
        generate_report_use_case: GenerateBillingReport,
    ):
        self.db = db
        self.call_gateway = call_gateway
        self.generate_report_use_case = generate_report_use_case
    
    def execute(self, filter: BillInputDTO):
        month = None
        year = None
        if filter.billing_period:
            period = filter.billing_period.split('/')
            month = int(period[0])
            year = int(period[1])
            today = datetime.now()
            if month == today.month and year == today.year:
                raise InvalidParam("Invalid period!")
        
        return self.generate_report_use_case.execute(self.db, self.call_gateway, filter.subscriber, year, month)
