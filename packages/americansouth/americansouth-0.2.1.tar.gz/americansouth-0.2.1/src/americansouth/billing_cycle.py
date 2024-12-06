import datetime


class BillingCycle:
    START_HOUR: int = 0
    START_MINUTE: int = 0
    START_SECOND: int = 0

    @classmethod
    def get_next_cycle_start(cls, dt: datetime.datetime) -> datetime.datetime:
        if dt.month == 12:
            year: int = dt.year + 1
            month: int = 1
        else:
            year: int = dt.year
            month: int = dt.month + 1
        return datetime.datetime(
            year,
            month,
            1,
            cls.START_HOUR,
            cls.START_MINUTE,
            cls.START_SECOND,
            tzinfo=datetime.timezone.utc,
        )
