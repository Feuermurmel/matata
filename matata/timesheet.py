import datetime
import pathlib
import re
from typing import List, NamedTuple

from matata.util import log, UserError


class TimeSheetEntry(NamedTuple):
    date: datetime.date
    start_time: datetime.time
    end_time: datetime.time

    def __repr__(self):
        date_str = self.date.isoformat()
        start_time = self.start_time.isoformat('minutes')
        end_time = self.end_time.isoformat('minutes')

        return f'TimeSheetEntry({date_str}, {start_time}, {end_time})'


class TimeSheet(NamedTuple):
    entries: List[TimeSheetEntry]


def _parse_time(time_str):
    match = re.fullmatch(
        '(?P<hour>[0-9]+)'
        '(\\.(?P<decihour>[0-9])|:(?P<minute>[0-9]{2}))?',
        time_str)

    if not match:
        raise UserError(f'Invalid time specification: {time_str}')

    hour = int(match.group('hour'))

    decihour_str = match.group('decihour')
    minute_str = match.group('minute')

    if decihour_str:
        minute = int(decihour_str) * 6
    elif minute_str:
        minute = int(minute_str)
    else:
        minute = 0

    return datetime.time(hour, minute)


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
