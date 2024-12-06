import datetime


class UsageCalculator:
    @staticmethod
    def calc_daily_limit(
        amount: float,
        total: float,
        hours_remaining: float,
    ) -> float:
        remaining_gb: float = total - amount
        days_remaining: float = hours_remaining / 24

        if days_remaining < 1:
            return remaining_gb

        return remaining_gb / days_remaining

    @staticmethod
    def calc_hours_remaining(
        current_time: datetime.datetime, next_billing: datetime.datetime
    ) -> float:
        return (next_billing - current_time).total_seconds() / 3600
