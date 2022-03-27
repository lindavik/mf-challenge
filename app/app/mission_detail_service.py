import logging
from typing import Dict


class MissionDetails(object):

    def __init__(self, autonomy: int, departure: str, arrival: str, routes):
        self.autonomy = autonomy
        self.departure = departure
        self.arrival = arrival
        self.routes = routes

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, MissionDetails):
            return (self.autonomy == other.autonomy and
                    self.departure == other.departure and
                    self.arrival == other.arrival)
        #todo add routes

        return False


class MissionConverter:

    @staticmethod
    def get_mission_details(details: Dict) -> MissionDetails:
        autonomy = MissionConverter._get_field(details=details, field_name="autonomy")
        if not (autonomy > 0):
            logging.exception(f"autonomy must be a greater than 0; however, was: {autonomy}")
            raise Exception("autonomy must be a greater than 0")
        departure = MissionConverter._get_field(details=details, field_name="departure")
        arrival = MissionConverter._get_field(details=details, field_name="arrival")
        routes = MissionConverter._get_field(details=details, field_name="routes_db")

        return MissionDetails(autonomy=autonomy, departure=departure, arrival=arrival, routes=routes)

    @staticmethod
    def _get_field(details: Dict, field_name: str):
        field = details.get(field_name)
        if not field:
            logging.exception(f"{field} Field must be provided")
            raise Exception(f"{field} Field must be provided")
        return field
