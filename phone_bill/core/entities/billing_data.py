from datetime import datetime, time


class BillingData:
    type: str
    base_price: int
    minute_fee: int
    start_time: time
    end_time: time

    def __init__(
        self,
        type: str,
        base_price: int,
        minute_fee: int,
        start_time: time,
        end_time: time,
    ):
        self.type = type
        self.base_price = base_price
        self.minute_fee = minute_fee
        self.start_time = start_time
        self.end_time = end_time
