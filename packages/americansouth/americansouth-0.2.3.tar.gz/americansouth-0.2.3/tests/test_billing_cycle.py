import datetime

from americansouth.billing_cycle import BillingCycle


def test_get_next_cycle_start():
    # Test mid-month date
    current = datetime.datetime(2024, 6, 15, 12, 30, tzinfo=datetime.timezone.utc)
    next_cycle = BillingCycle.get_next_cycle_start(current)
    assert next_cycle == datetime.datetime(
        2024, 7, 1, 0, 0, 0, tzinfo=datetime.timezone.utc
    )

    # Test end of year
    current = datetime.datetime(2024, 12, 25, 12, 30, tzinfo=datetime.timezone.utc)
    next_cycle = BillingCycle.get_next_cycle_start(current)
    assert next_cycle == datetime.datetime(
        2025, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc
    )
