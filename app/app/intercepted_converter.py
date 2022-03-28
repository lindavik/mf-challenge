import logging
from typing import Dict, List

from app.mission_detail_service import FieldConverter


class InterceptedData(object):
    def __init__(self, countdown: int, bounty_hunter_schedule: Dict):
        self.countdown: int = countdown
        self.bounty_hunter_schedule: Dict = bounty_hunter_schedule

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, InterceptedData):
            return (self.countdown == other.countdown and
                    self.bounty_hunter_schedule == other.bounty_hunter_schedule)

        return False


class InterceptedDataConverter(FieldConverter):
    @staticmethod
    def map_to_intercepted_data(raw_data):
        countdown_field_name = "countdown"
        countdown: int = InterceptedDataConverter._get_field(details=raw_data, field_name=countdown_field_name)
        InterceptedDataConverter._validate_positive_integer(field=countdown, field_name=countdown_field_name)
        bounty_hunter_schedule_raw: List = InterceptedDataConverter._get_field(details=raw_data,
                                                                               field_name="bounty_hunters")
        bounty_hunter_schedule: Dict = InterceptedDataConverter._process_schedule(
            raw_schedule=bounty_hunter_schedule_raw)
        return InterceptedData(countdown=countdown, bounty_hunter_schedule=bounty_hunter_schedule)

    @staticmethod
    def _process_schedule(raw_schedule: List) -> Dict:
        schedule = {}
        for item in raw_schedule:
            key = item["planet"]
            if key not in schedule.keys():
                schedule[key] = {item["day"]}
            else:
                schedule[key].add(item["day"])
        return schedule
