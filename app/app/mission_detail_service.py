import logging
from collections import defaultdict
from typing import Dict

from app.db_connector import DBConnector


class PlanetGraph(object):
    def __init__(self):
        self.planets = set()
        self.routes = defaultdict(list)
        self.distances = {}

    def add_planet(self, planet_name: str):
        self.planets.add(planet_name)

    def add_route(self, departure_planet: str, destination_planet: str, distance: int):
        self.add_planet(departure_planet)
        self.add_planet(destination_planet)
        self.routes[departure_planet].append(destination_planet)
        self.routes[destination_planet].append(departure_planet)
        self.distances[(departure_planet, destination_planet)] = distance
        self.distances[(destination_planet, departure_planet)] = distance

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, PlanetGraph):
            return (self.planets == other.planets and
                    self.routes == other.routes and
                    self.distances == other.distances)


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
                    self.arrival == other.arrival and
                    self.routes == other.routes)

        return False


class MissionConverter:

    @staticmethod
    def map_to_mission_details(details: Dict, directory: str) -> MissionDetails:
        autonomy = MissionConverter._get_field(details=details, field_name="autonomy")
        if not isinstance(autonomy, int):
            logging.exception(f"autonomy must be an int; however, was: {type(autonomy)}")
            raise Exception("autonomy must be an integer")
        elif not (autonomy > 0):
            logging.exception(f"autonomy must be a greater than 0; however, was: {autonomy}")
            raise Exception("autonomy must be a greater than 0")
        departure = MissionConverter._get_field(details=details, field_name="departure")
        arrival = MissionConverter._get_field(details=details, field_name="arrival")

        planet_db_file = MissionConverter._get_field(details=details, field_name="routes_db")
        planet_db_file = f"{directory}/{planet_db_file}"
        planet_graph: PlanetGraph = MissionConverter._load_routes(planet_db_file)

        return MissionDetails(autonomy=autonomy, departure=departure, arrival=arrival, routes=planet_graph)

    @staticmethod
    def _get_field(details: Dict, field_name: str):
        field = details.get(field_name)
        if not field:
            logging.exception(f"{field} Field must be provided")
            raise Exception(f"{field} Field must be provided")
        return field

    @staticmethod
    def _load_routes(db_file: str) -> PlanetGraph:
        routes = MissionConverter.get_routes(db_file)
        planet_graph = PlanetGraph()
        for route in routes:
            planet_graph.add_route(departure_planet=route[0], destination_planet=route[1], distance=route[2])
        return planet_graph

    @staticmethod
    def get_routes(db_file: str):
        route_query: str = "SELECT origin, destination, travel_time FROM routes"
        return DBConnector.get_iterator(db_file=db_file, query=route_query)