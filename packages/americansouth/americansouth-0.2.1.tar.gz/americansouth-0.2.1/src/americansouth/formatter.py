import datetime
import zoneinfo


class DataFormatter:
    @staticmethod
    def format_gb(gb: float) -> str:
        return f"{int(gb)}GB"

    @staticmethod
    def format_time(dt: datetime.datetime) -> str:
        pst_time: datetime.datetime = dt.astimezone(
            zoneinfo.ZoneInfo("America/Los_Angeles")
        )
        return (
            pst_time.strftime("%a %b %d %I:%M %p %Y")
            .replace(" PM", "pm")
            .replace(" AM", "am")
        )
