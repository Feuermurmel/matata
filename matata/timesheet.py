import datetime
import pathlib
from typing import List, NamedTuple, Optional

from matata.util import log


class TimeSheetEntry(NamedTuple):
    date: datetime.date
    start_time: datetime.time
    end_time: datetime.time


class TimeSheet(NamedTuple):
    entries: List[TimeSheetEntry]


def _parse_time(time_str):
    seconds = round(float(time_str) * 3600)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)

    return datetime.time(hours, minutes, seconds)


def read_time_sheet(path: pathlib.Path):
    def iter_entries():
        with path.open(encoding='utf-8') as file:
            for i in file:
                line, *_ = i.split('#', 1)

                if line.strip():
                    date_str, *range_strs = line.split()

                    date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()

                    while range_strs:
                        if len(range_strs) < 2:
                            log(f'warning: Line contains an incomplete time range: {i}')

                            break

                        start_str, end_str, *range_strs = range_strs

                        yield TimeSheetEntry(date, _parse_time(start_str), _parse_time(end_str))

    return TimeSheet(list(iter_entries()))



