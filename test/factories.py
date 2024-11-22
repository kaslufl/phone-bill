import string
from datetime import datetime, time

import factory
import factory.fuzzy

from phone_bill.core.external.schema import BillingORM, BillingType, CallORM


class BillingFactory(factory.Factory):
    class Meta:
        model = BillingORM

    type = factory.fuzzy.FuzzyChoice(BillingType)
    base_price = 10
    minute_fee = 1
    start_time = time(6, 0)
    end_time = time(22, 0)


class CallFactory(factory.Factory):
    class Meta:
        model = CallORM

    id = 1
    source = 9999999999
    destination = factory.fuzzy.FuzzyText(length=10, chars=string.digits)
    price = 100
    start_timestamp = datetime(2024, 11, 22, 21)
    end_timestamp = datetime(2024, 11, 22, 23)
