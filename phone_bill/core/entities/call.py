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
        remaining_duration = int((self.end_timestamp - self.start_timestamp).total_seconds())

        sorted_periods = self._sort_periods(billing_periods)
        price = sorted_periods[0].base_price

        while remaining_duration > 0:
            for period in sorted_periods:
                start = datetime.combine(current_time.date(), period.start_time)
                end = datetime.combine(current_time.date(), period.end_time)

                if start > end and start > current_time:
                    start = start - timedelta(days=1)
                
                elif start > end and start <= current_time:
                    end = end + timedelta(days=1)

                time_in_period = timedelta(0)
                if start <= current_time <= end:
                    next_transition = min(self.end_timestamp, end)
                    time_in_period = next_transition - current_time
                    current_time = next_transition

                remaining_duration -= time_in_period.seconds
                price += (time_in_period.seconds // 60) * period.minute_fee

        self.price = price

    def _sort_periods(
        self, billing_periods: list[BillingData]
    ) -> list[BillingData]:

        def find_period(periods: list[BillingData]):
            for i, periods[i] in enumerate(periods):
                period_start = datetime.combine(self.start_timestamp.date(), periods[i].start_time)
                period_end = datetime.combine(self.start_timestamp.date(), periods[i].end_time)

                if period_start > period_end and period_start > self.start_timestamp: 
                    period_start = period_start - timedelta(days=1)
                
                elif period_start > period_end and period_start < self.start_timestamp: 
                    period_end = period_end + timedelta(days=1)
                    
                if period_start <= self.start_timestamp <= period_end:
                    return i

        billing_periods.sort(key=lambda period: period.start_time)
        start_index = find_period(billing_periods)

        return billing_periods[start_index:] + billing_periods[:start_index]
