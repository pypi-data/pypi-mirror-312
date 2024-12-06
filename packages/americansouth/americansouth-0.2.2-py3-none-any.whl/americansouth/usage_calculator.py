import datetime

from .constants import SECONDS_PER_DAY


class UsageCalculator:
    @staticmethod
    def calc_daily_limit(
        amount: float,
        total: float,
        seconds_remaining: float,
    ) -> float:
        remaining_gb: float = total - amount
        days_remaining: float = seconds_remaining / SECONDS_PER_DAY

        if days_remaining < 1:
            return remaining_gb

        return remaining_gb / days_remaining

    @staticmethod
    def calc_hours_remaining(
        current_time: datetime.datetime, next_billing: datetime.datetime
    ) -> float:
        return (next_billing - current_time).total_seconds()
