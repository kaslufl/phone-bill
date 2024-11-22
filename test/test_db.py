from dataclasses import asdict
from datetime import datetime

from sqlalchemy import select

from phone_bill.core.external.schema import CallORM


def test_create_call(session):
    time = datetime.now()

    new_call = CallORM(
        id=1,
        start_timestamp=time,
        end_timestamp=time,
        source="321",
        destination="123",
        price=100,
    )

    session.add(new_call)
    session.commit()

    call = session.scalar(select(CallORM).where(CallORM.id == 1))

    assert asdict(call) == {
        "id": 1,
        "start_timestamp": time,
        "end_timestamp": time,
        "source": "321",
        "destination": "123",
        "price": 100,
    }
