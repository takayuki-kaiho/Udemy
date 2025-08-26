# app/utils.py
from datetime import timedelta, date as date_cls, datetime as dt

def _to_date(value):
    """datetimeやdateを必ずdate型に変換"""
    if value is None:
        return None
    if isinstance(value, date_cls) and not isinstance(value, dt):
        return value
    if isinstance(value, dt):
        return value.date()
    return None

def business_day_count(start, end, holidays=set()):
    """start～end の間の稼働日数（土日・祝日を除外）。両端含む。"""
    start = _to_date(start)
    end   = _to_date(end)

    if not start or not end:
        return None

    if start > end:
        start, end = end, start

    days = 0
    cur = start
    while cur <= end:
        if cur.weekday() < 5 and cur not in holidays:  # 0=Mon .. 6=Sun
            days += 1
        cur += timedelta(days=1)
    return days
