import os
from typing import List

from app.file_reader import FileReader
from app.mission_detail_service import MissionConverter, MissionDetails


class MissionDetailsDTO:
    def __init__(self, autonomy: int, departure: str, arrival: str, routes):
        self.autonomy = autonomy
        self.departure = departure
        self.arrival = arrival
        self.routes = routes

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, MissionDetailsDTO):
            return (self.autonomy == other.autonomy and
                    self.departure == other.departure and
                    self.arrival == other.arrival and
                    self.routes == other.routes)

        return False


# {
#   "countdown": 6,
#   "bounty_hunters": [
#     {"planet": "Tatooine", "day": 4 },
#     {"planet": "Dagobah", "day": 5 }
#   ]
# }
#
#
# class BountyHunterDTO:
#     def __init__(self, planet: str, day: int):
#         self.planet = countdown
#         self.bounty_hunters = bounty_hunters


class InterceptedDataDTO:
    def __init__(self, countdown: int, bounty_hunters: List):
        self.countdown = countdown
        self.bounty_hunters = bounty_hunters

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, InterceptedDataDTO):
            return (self.countdown == other.countdown and
                    self.bounty_hunters == other.bounty_hunters)

        return False


class ContextLoader:

    @staticmethod
    def load_mission_details(file_path: str):
        mission_details_raw = FileReader.read_json(file_path)
        directory: str = os.path.dirname(file_path)
        mission_details: MissionDetails = MissionConverter.map_to_mission_details(mission_details_raw, directory)
        return mission_details

    @staticmethod
    def load_intercepted_data(file):
        raw_intercepted_data = FileReader.read_json(file)
        pass