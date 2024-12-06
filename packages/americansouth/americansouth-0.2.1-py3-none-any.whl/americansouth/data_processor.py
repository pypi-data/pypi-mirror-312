import datetime
import typing
import zoneinfo

from .billing_cycle import BillingCycle
from .repository import Repository
from .usage_calculator import UsageCalculator


class DataProcessor:
    def __init__(self, repository: Repository) -> None:
        self.repository = repository
        self.billing_cycle = BillingCycle()
        self.usage_calculator = UsageCalculator()

    def _parse_datetime(self, dt_str: str) -> datetime.datetime:
        try:
            dt = datetime.datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
            return dt.replace(tzinfo=zoneinfo.ZoneInfo("UTC"))
        except ValueError:
            dt = datetime.datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%S.%fZ")
            return dt.replace(tzinfo=zoneinfo.ZoneInfo("UTC"))

    def process_data(
        self,
    ) -> typing.List[typing.Tuple[float, float, datetime.datetime, float, float]]:
        amount_groups: typing.Dict[
            float, typing.Tuple[datetime.datetime, float, float, float]
        ] = {}

        for record in self.repository.load():
            amount: float = float(record["amount"])
            total: float = float(record["total"])
            scraped_at: datetime.datetime = self._parse_datetime(record["scrapedAt"])

            if amount not in amount_groups or scraped_at > amount_groups[amount][0]:
                next_billing: datetime.datetime = (
                    self.billing_cycle.get_next_cycle_start(scraped_at)
                )
                hours_remaining: float = self.usage_calculator.calc_hours_remaining(
                    scraped_at, next_billing
                )
                daily_limit: float = self.usage_calculator.calc_daily_limit(
                    amount, total, hours_remaining
                )
                amount_groups[amount] = (
                    scraped_at,
                    hours_remaining,
                    daily_limit,
                    total,
                )

        records: typing.List[
            typing.Tuple[float, float, datetime.datetime, float, float]
        ] = [
            (hours, amount, scraped_at, daily_limit, total)
            for amount, (scraped_at, hours, daily_limit, total) in amount_groups.items()
        ]
        return sorted(records, key=lambda x: x[2])
