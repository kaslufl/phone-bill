from sqlalchemy.orm import Session

from phone_bill.core.external.repository.ibilling_repository import IBillingRepository


class BillingGateway:
    repository: IBillingRepository

    def __init__(self, repository: IBillingRepository):
        self.repository = repository

    def get_billing_periods(self, db: Session):
        return self.repository.get_billing_periods(db)
