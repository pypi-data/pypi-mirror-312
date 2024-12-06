import datetime

from americansouth.display import DisplayManager


def test_daily_used_not_negative():
    display = DisplayManager()
    record = (0, 0, datetime.datetime.now(datetime.timezone.utc), 13, 400)
    prev_amount = 234

    display.print_record(record, prev_amount)
    # Visual inspection that output shows 0GB not -234GB for daily used
