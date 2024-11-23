from datetime import time
from sqlalchemy.orm import Session

from phone_bill.core.entities.call import Call
from phone_bill.core.external.repository.call_repository import ICallRepository


class CallGateway:
    repository: ICallRepository

    def __init__(self, repository: ICallRepository):
        self.repository = repository

    def get_call(self, db: Session, call_id: int):
        return self.repository.get_call(db, call_id)

    def insert_call(self, db: Session, data: Call):
        return self.repository.insert_call(db, data)

    def update_call(self, db: Session, data: Call):
        return self.repository.update_call(db, data)

    def get_billing(self, db: Session, subscriber: str, period: time):
        return self.repository.get_billing(db, subscriber, period)
