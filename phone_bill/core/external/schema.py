from datetime import datetime, time
from enum import Enum

from sqlalchemy import DateTime, Integer, String, Time
from sqlalchemy.orm import Mapped, mapped_column, registry

table_registry = registry()


@table_registry.mapped_as_dataclass
class CallORM:
    __tablename__ = "call"

    id: Mapped[int] = mapped_column(init=True, primary_key=True)
    start_timestamp: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    end_timestamp: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    source: Mapped[str | None] = mapped_column(String, nullable=True)
    destination: Mapped[str | None] = mapped_column(String, nullable=True)
    price: Mapped[int | None] = mapped_column(Integer, nullable=True)


class BillingType(str, Enum):
    peak = "PEAK"
    off_peak = "OFF PEAK"


@table_registry.mapped_as_dataclass
class BillingORM:
    __tablename__ = "billing"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    type: Mapped[BillingType]
    base_price: Mapped[int]
    minute_fee: Mapped[int]
    start_time: Mapped[time] = mapped_column(Time, nullable=False)
    end_time: Mapped[time] = mapped_column(Time, nullable=False)
