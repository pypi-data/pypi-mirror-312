import datetime
import typing

from .formatter import DataFormatter


class DisplayManager:
    def __init__(self) -> None:
        self.formatter: DataFormatter = DataFormatter()
        self.headers: typing.Dict[str, str] = {
            "daily": "DAILY USED",
            "budget": "DAILY BUDGET",
            "total": "BANDWIDTH USED",
            "monthly": "REMAINING BUDGET",
            "total_avail": "MONTHLY BUDGET",
            "fetch": "DATA FETCH TIME",
        }
        self.col_width: typing.Dict[str, int] = {
            "daily": len(self.headers["daily"]),
            "budget": len(self.headers["budget"]),
            "total": len(self.headers["total"]),
            "monthly": len(self.headers["monthly"]),
            "total_avail": len(self.headers["total_avail"]),
            "fetch": len(self.headers["fetch"]),
        }

    def update_widths(
        self,
        records: typing.List[
            typing.Tuple[float, float, datetime.datetime, float, float]
        ],
    ) -> None:
        prev_amount = 0
        for record in records:
            _, amount, scraped_at, daily_limit, total = record
            daily_used = amount - prev_amount
            remaining = total - amount

            daily_str = f"{int(daily_used)}GB"
            budget_str = self.formatter.format_gb(daily_limit)
            total_str = f"{int(amount)}GB"
            remaining_str = f"{int(remaining)}GB"
            total_avail_str = f"{int(total)}GB"
            fetch_time = self.formatter.format_time(scraped_at)

            self.col_width["daily"] = max(self.col_width["daily"], len(daily_str))
            self.col_width["budget"] = max(self.col_width["budget"], len(budget_str))
            self.col_width["total"] = max(self.col_width["total"], len(total_str))
            self.col_width["monthly"] = max(
                self.col_width["monthly"], len(remaining_str)
            )
            self.col_width["total_avail"] = max(
                self.col_width["total_avail"], len(total_avail_str)
            )
            self.col_width["fetch"] = max(self.col_width["fetch"], len(fetch_time))

            prev_amount = amount

    def print_headers(self) -> None:
        print(
            f"{self.headers['daily']:>{self.col_width['daily']}} "
            f"{self.headers['budget']:>{self.col_width['budget']}} "
            f"{self.headers['total']:>{self.col_width['total']}} "
            f"{self.headers['monthly']:>{self.col_width['monthly']}} "
            f"{self.headers['total_avail']:>{self.col_width['total_avail']}} "
            f"{self.headers['fetch']:<{self.col_width['fetch']}}"
        )
        total_width = sum(self.col_width.values()) + len(self.col_width) - 1
        print("-" * total_width)

    def print_record(
        self,
        record: typing.Tuple[float, float, datetime.datetime, float, float],
        prev_amount: float,
    ) -> None:
        _, amount, scraped_at, daily_limit, total = record
        daily_used: float = amount - prev_amount
        remaining: float = total - amount
        daily_str: str = f"{int(daily_used)}GB"
        total_str: str = f"{int(amount)}GB"
        remaining_str: str = f"{int(remaining)}GB"
        total_avail_str: str = f"{int(total)}GB"
        fetch_time: str = self.formatter.format_time(scraped_at)
        print(
            f"{daily_str:>{self.col_width['daily']}} "
            f"{self.formatter.format_gb(daily_limit):>{self.col_width['budget']}} "
            f"{total_str:>{self.col_width['total']}} "
            f"{remaining_str:>{self.col_width['monthly']}} "
            f"{total_avail_str:>{self.col_width['total_avail']}} "
            f"{fetch_time:<{self.col_width['fetch']}}"
        )
