import argparse
import datetime
import pathlib
import sys

from matata.hakuna import API, TimeEntry
from matata.timesheet import read_time_sheet, TimeSheetEntry
from matata.util import UserError, log


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--site')
    parser.add_argument('--api-key')
    parser.add_argument('--num-past-days', type=int, default=30)
    parser.add_argument('time_sheet', type=pathlib.Path)

    return parser.parse_args()


def time_sheet_entry_from_hakuna_entry(entry: TimeEntry):
    return TimeSheetEntry(entry.date, entry.start_time, entry.end_time)


def entry_point(parse_args_fn):
    def decorator(main_fn):
        def wrapped_fn():
            try:
                main_fn(**vars(parse_args_fn()))
            except KeyboardInterrupt:
                log('Operation interrupted.')
                sys.exit(1)
            except UserError as e:
                log(f'error: {e}')
                sys.exit(2)

        return wrapped_fn

    return decorator


@entry_point(parse_args)
def main(site, api_key, num_past_days, time_sheet):
    api = API(site, api_key)

    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=num_past_days)

    ts = timesheet.read_time_sheet(time_sheet)
    time_sheet_entry_set = \
        set(i for i in ts.entries if start_date <= i.date <= end_date)

    existing_hakuna_entries = api.list_time_entries(start_date, end_date)

    for i in sorted(existing_hakuna_entries):
        time_sheet_entry = time_sheet_entry_from_hakuna_entry(i)

        if time_sheet_entry in time_sheet_entry_set:
            # Remove from the local set so that the remaining entries are the
            # ones missing from Hakuna.
            time_sheet_entry_set.remove(time_sheet_entry)
        else:
            log(f'Deleting entry: {time_sheet_entry}')

            # Remote entries we don't have in the local time sheet from Hakuna.
            api.delete_time_entry(i.id)

    for i in sorted(time_sheet_entry_set):
        log(f'Creating entry: {i}')

        api.create_time_entry(i.date, i.start_time, i.end_time, task_id=1)


@entry_point(lambda: argparse.ArgumentParser().parse_args())
def date_list_main():
    start = datetime.date.today()
    start -= datetime.timedelta(start.weekday())

    for i in range(7 * 52):
        day = start + datetime.timedelta(days=i)

        print(f'{day}  ')

        if day.weekday() == 6:
            print()
