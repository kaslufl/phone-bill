from datetime import datetime, time
from test.factories import BillingFactory

from phone_bill.core.entities.call import Call


def test_calculate_price_call_within_single_period():
    billings_periods = []
    billings_periods.append(BillingFactory())

    call = Call(100, datetime(2024, 11, 22, 10), datetime(2024, 11, 22, 11))

    call.calculate_price(billings_periods)
    assert call.price == 70


def test_calculate_price_call_across_multiple_periods():
    billings_periods = []
    billings_periods.append(BillingFactory())
    billings_periods.append(
        BillingFactory(start_time=time(22, 0), end_time=time(6, 0), minute_fee=2)
    )

    call = Call(100, datetime(2024, 11, 22, 21), datetime(2024, 11, 22, 23))

    call.calculate_price(billings_periods)
    assert call.price == 190


def test_calculate_price_call_across_multiple_periods_shouldnt_consider_all_periods():
    billings_periods = []
    billings_periods.append(BillingFactory())
    billings_periods.append(
        BillingFactory(start_time=time(22, 0), end_time=time(2, 0), minute_fee=2)
    )
    billings_periods.append(
        BillingFactory(start_time=time(2, 0), end_time=time(6, 0), minute_fee=3)
    )

    call = Call(100, datetime(2024, 11, 22, 21), datetime(2024, 11, 22, 23))

    call.calculate_price(billings_periods)
    assert call.price == 190
