from sqlalchemy.orm import Session

from phone_bill.core.external.repository.ibilling_repository import IBillingRepository
from phone_bill.core.external.schema import BillingORM


class BillingRepository(IBillingRepository):

    def get_billing_periods(db: Session):
        periods: list[BillingORM] = db.query(BillingORM).all()
        return periods
