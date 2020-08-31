import datetime
import urllib.parse
from typing import NamedTuple

import requests


class TimeEntry(NamedTuple):
    id: int
    date: datetime.date
    start_time: datetime.time
    end_time: datetime.time


class API:
    def __init__(self, site_url: str, api_token: str):
        self.site_url = site_url
        self.api_token = api_token

    def list_time_entries(self, start_date: datetime.date, end_date: datetime.date):
        response = requests.get(
            urllib.parse.urljoin(self.site_url, 'api/v1/time_entries'),
            params=dict(start_date=start_date.isoformat(), end_date=end_date.isoformat()),
            headers={'X-Auth-Token': self.api_token})

        response.raise_for_status()

        def iter_time_entries():
            for i in response.json():
                yield TimeEntry(
                    id=int(i['id']),
                    date=datetime.date.fromisoformat(i['date']),
                    start_time=datetime.time.fromisoformat(i['start_time']),
                    end_time=datetime.time.fromisoformat(i['end_time']))

        return list(iter_time_entries())

    def create_time_entry(self, date: datetime.date, start_time: datetime.time, end_time: datetime.time, task_id: int):
        response = requests.post(
            urllib.parse.urljoin(self.site_url, 'api/v1/time_entries'),
            params=dict(
                date=date.isoformat(),
                start_time=start_time.isoformat('minutes'),
                end_time=end_time.isoformat('minutes'),
                task_id=task_id),
            headers={'X-Auth-Token': self.api_token})

        response.raise_for_status()

        return response.json()

    def delete_time_entry(self, id: int):
        response = requests.delete(
            urllib.parse.urljoin(self.site_url, f'api/v1/time_entries/{id}'),
            headers={'X-Auth-Token': self.api_token})

        response.raise_for_status()
