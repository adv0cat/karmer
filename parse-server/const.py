import os

from datetime import timedelta


def get_max_offset() -> timedelta:
    weeks = int(os.environ.get("OFFSET_WEEKS") or '0')
    days = int(os.environ.get("OFFSET_DAYS") or '0')
    hours = int(os.environ.get("OFFSET_HOURS") or '0')
    minutes = int(os.environ.get("OFFSET_MINUTES") or '0')
    max_offset = timedelta(weeks=weeks, days=days, hours=hours, minutes=minutes)
    if max_offset < timedelta(minutes=1):
        max_offset = timedelta(days=1)

    return max_offset
