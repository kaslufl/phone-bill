from datetime import date

from sqlalchemy import and_, extract
from sqlalchemy.orm import Session

from phone_bill.core.entities.call import Call
from phone_bill.core.external.repository.icall_repository import ICallRepository
from phone_bill.core.external.schema import CallORM


class CallRepository(ICallRepository):

    def get_call(db: Session, call_id: int):
        call_history: Call = db.get(CallORM, call_id)
        return call_history

    def insert_call(db: Session, call: Call):
        call_history: CallORM = CallORM(**{**call.__dict__})

        db.add(call_history)
        db.commit()
        db.refresh(call_history)

        return call_history

    def update_call(db: Session, call: CallORM):

        db.commit()

        return call

    def update_call_price(db: Session, call: CallORM):

        db.query(CallORM).filter(CallORM.id == call.id).update({CallORM.price : call.price})
        db.commit()

        return call

    def get_billing(db: Session, source: str, period: date):
        billing: list[CallORM] = db.query(CallORM).filter(
            and_(
                CallORM.source == source,
                CallORM.start_timestamp != None,
                CallORM.end_timestamp != None,
                extract('year', CallORM.end_timestamp) == period.year,
                extract('month', CallORM.end_timestamp) == period.month,
            )
        ).all()
        return billing
