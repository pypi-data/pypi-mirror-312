# -*- coding: utf-8 -*-

from calendar import monthrange, timegm
from datetime import datetime, timedelta
from enum import Enum
from typing import Tuple, Iterator

from dateutil.rrule import MONTHLY
from dateutil.rrule import rrule


class FrequencyType(Enum):
    HOUR = "HOUR"
    MONTH = "MONTH"
    DAY = "DAY"


def get_time_windows(
        start: str, end: str = None, frequency: FrequencyType = None,
        utc: bool = True) -> Iterator[Tuple]:

    """
    It returns an iterator which contains a list of tuples (init, end) starting
    from the "start" datetime...
    """

    now_fcn = datetime.utcnow if utc else datetime.now

    if not frequency:
        yield start, now_fcn().strftime("%Y-%m-%dT%H:%M:%S")

    start = datetime.fromisoformat(start).replace(minute=0, second=0, microsecond=0)
    end = (now_fcn() if not end else datetime.fromisoformat(end)).replace(minute=0, second=0, microsecond=0)

    if frequency in [FrequencyType.HOUR, FrequencyType.DAY]:
        if frequency == FrequencyType.HOUR:
            delta = timedelta(hours=1)

        else:
            start, end = start.replace(hour=0), end.replace(hour=0)
            delta = timedelta(days=1)

        while start < end and (start + delta) <= end:
            yield (start.strftime("%Y-%m-%dT%H:%M:%S"), start.strftime("%Y-%m-%dT%H:59:59")) \
                if frequency == FrequencyType.HOUR \
                else (start.strftime("%Y-%m-%dT%H:%M:%S"), start.strftime("%Y-%m-%dT23:59:59"))

            start = start + delta

    elif frequency == FrequencyType.MONTH:
        end = end.replace(hour=0)

        for d in rrule(MONTHLY, dtstart=start, until=end):
            start_ = datetime(year=d.year, month=d.month, day=1)
            end_ = start_.replace(day=monthrange(start_.year, start_.month)[1])
            if end_ <= end:
                yield start_.strftime("%Y-%m-%dT%H:%M:%S"), end_.strftime("%Y-%m-%dT23:59:59")


def utc_datetime_to_epoch(timestamp: datetime):
    return timegm(timestamp.utctimetuple())
