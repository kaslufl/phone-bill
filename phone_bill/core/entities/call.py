from datetime import datetime, timedelta
from typing import Optional

from phone_bill.core.entities.billing_data import BillingData


class Call:
    def __init__(
        self,
        id: int,
        start_timestamp: Optional[datetime] = None,
        end_timestamp: Optional[datetime] = None,
        source: Optional[str] = None,
        destination: Optional[str] = None,
        price: Optional[int] = None,
    ):
        self.id = id
        self.start_timestamp = start_timestamp
        self.end_timestamp = end_timestamp
        self.source = source
        self.destination = destination
        self.price = price

    def calculate_price(self, billing_periods: list[BillingData]):
        current_time = self.start_timestamp

        sorted_periods = self._sort_periods(billing_periods, current_time)
        price = sorted_periods[0].base_price

        for period in sorted_periods:
            start = datetime.combine(self.start_timestamp.date(), period.start_time)
            end = datetime.combine(self.start_timestamp.date(), period.end_time)

            if end < start:
                end += timedelta(1)

            time_in_period = timedelta(0)
            if start <= current_time <= end:
                next_transition = min(self.end_timestamp, end)
                time_in_period = next_transition - current_time
                current_time = next_transition

            price += (time_in_period.seconds // 60) * period.minute_fee

        self.price = price

    def _sort_periods(
        self, billing_periods: list[BillingData], start
    ) -> list[BillingData]:

        def find_period(periods: list[BillingData], start):
            for i, period in enumerate(periods):
                if period.start_time <= start.time() < period.end_time:
                    return i

        billing_periods.sort(key=lambda period: period.start_time)
        start_index = find_period(billing_periods, start)

        return billing_periods[start_index:] + billing_periods[0 : start_index - 1]
