import datetime

from americansouth.usage_calculator import UsageCalculator


def test_calc_daily_limit_comprehensive():
    calculator = UsageCalculator()

    limit = calculator.calc_daily_limit(
        amount=100.0,
        total=400.0,
        hours_remaining=240.0,
    )
    assert round(limit, 2) == 30.0

    limit = calculator.calc_daily_limit(
        amount=234.0,
        total=400.0,
        hours_remaining=4.0,
    )
    remaining_gb = 400.0 - 234.0
    assert limit == remaining_gb
    assert limit <= remaining_gb

    limit = calculator.calc_daily_limit(
        amount=234.0,
        total=400.0,
        hours_remaining=1.0,
    )
    assert limit == 400.0 - 234.0

    limit = calculator.calc_daily_limit(
        amount=234.0,
        total=400.0,
        hours_remaining=0.33,
    )
    assert limit == 400.0 - 234.0

    limit = calculator.calc_daily_limit(
        amount=200.0,
        total=400.0,
        hours_remaining=24.0,
    )
    assert limit == 400.0 - 200.0

    limit = calculator.calc_daily_limit(
        amount=200.0,
        total=400.0,
        hours_remaining=25.0,
    )
    assert limit < 400.0 - 200.0
    assert round(limit, 2) == round((400.0 - 200.0) / (25.0 / 24.0), 2)


def test_calc_daily_limit_edge_cases():
    calculator = UsageCalculator()

    # Test normal case
    limit = calculator.calc_daily_limit(
        amount=100.0,
        total=400.0,
        hours_remaining=0.0,
    )
    assert limit == 300.0

    limit = calculator.calc_daily_limit(
        amount=400.0,
        total=400.0,
        hours_remaining=48.0,
    )
    assert limit == 0.0

    limit = calculator.calc_daily_limit(
        amount=0.0,
        total=400.0,
        hours_remaining=24.0 * 30,
    )
    assert round(limit, 2) == round(400.0 / 30, 2)


def test_calc_daily_limit_validation():
    calculator = UsageCalculator()

    test_cases = [
        (234.0, 400.0, 0.33),
        (100.0, 400.0, 240.0),
        (0.0, 400.0, 720.0),
        (399.0, 400.0, 48.0),
        (200.0, 400.0, 24.0),
    ]

    for amount, total, hours in test_cases:
        limit = calculator.calc_daily_limit(amount, total, hours)
        remaining = total - amount
        assert limit <= remaining
        assert limit >= 0


def test_calc_daily_limit_with_billing_cycle():
    calculator = UsageCalculator()

    current = datetime.datetime(2024, 11, 1, 0, 0, tzinfo=datetime.timezone.utc)
    next_billing = datetime.datetime(2024, 12, 1, 0, 0, tzinfo=datetime.timezone.utc)
    hours = calculator.calc_hours_remaining(current, next_billing)
    limit = calculator.calc_daily_limit(0.0, 400.0, hours)
    assert round(limit, 2) == round(400.0 / 30, 2)

    current = datetime.datetime(2024, 11, 30, 20, 0, tzinfo=datetime.timezone.utc)
    next_billing = datetime.datetime(2024, 12, 1, 0, 0, tzinfo=datetime.timezone.utc)
    hours = calculator.calc_hours_remaining(current, next_billing)
    limit = calculator.calc_daily_limit(234.0, 400.0, hours)
    assert limit == 400.0 - 234.0

    current = datetime.datetime(2024, 11, 15, 0, 0, tzinfo=datetime.timezone.utc)
    next_billing = datetime.datetime(2024, 12, 1, 0, 0, tzinfo=datetime.timezone.utc)
    hours = calculator.calc_hours_remaining(current, next_billing)
    limit = calculator.calc_daily_limit(200.0, 400.0, hours)
    expected_days = hours / 24
    assert round(limit, 2) == round((400.0 - 200.0) / expected_days, 2)
