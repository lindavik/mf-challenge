from collections import defaultdict, namedtuple
from typing import Dict, List

from givemetheodds.converters import PlanetGraph, MissionDetails


class PredictionService(object):

    def __init__(self, mission_details: MissionDetails):
        self.autonomy: int = mission_details.autonomy
        self.departure: str = mission_details.departure
        self.destination: str = mission_details.arrival
        self.planet_graph: PlanetGraph = mission_details.routes

    def get_probability_of_success(self, countdown: int, hunter_schedule: Dict) -> int:
        """
        Calculates the probability of successfully reaching the destination planet without
        being captured by bounty hunters. Returns a number ranging from 0 to 100.
        :param countdown: positive integer indicating the number of days before the Death Star annihilates Endor
        :param hunter_schedule: list of all locations where Bounty Hunter are scheduled to be present
        :return: a positive integer (0-100) indicating the probability (%) of successfully reaching the destination planet
        without being captured by bounty hunters
        """
        shortest_path = self._get_shortest_path_to_destination()
        adjusted_path = PredictionService._adjust_for_fuelling_needs(route=shortest_path, autonomy=self.autonomy)
        earliest_arrival_day = adjusted_path[-1][1]
        if earliest_arrival_day > countdown:
            return 0
        else:
            capture_attempt_count = PredictionService._get_capture_attempt_count(
                shortest_path=shortest_path, hunter_schedule=hunter_schedule
            )

            probability_of_capture: float = PredictionService._get_probability_of_capture(
                capture_attempt_count=capture_attempt_count
            )
            return PredictionService._convert_capture_probability_to_success_rate(
                probability_of_capture=probability_of_capture
            )

    def _get_shortest_path_to_destination(self):
        """
        Determines the shortest path from the departure planet to the destination planet.
        Disclaimer: provides with only one route, if there are two equally long shortest routes, only one will be returned.
        :return:
        """
        visited = {self.departure: 0}
        path = defaultdict(list)
        nodes = set(self.planet_graph.planets)

        while nodes:
            closest_node = None
            for node in nodes:
                if node in visited:
                    if closest_node is None:
                        closest_node = node
                    elif visited[node] < visited[closest_node]:
                        closest_node = node
            if closest_node is None:
                break

            nodes.remove(closest_node)
            current_distance_travelled = visited[closest_node]

            for edge in self.planet_graph.routes[closest_node]:

                new_distance = (
                        current_distance_travelled + self.planet_graph.distances[(closest_node, edge)]
                )

                if edge not in visited or new_distance < visited[edge]:
                    visited[edge] = new_distance
                    path[edge] = []
                    path[edge].append(closest_node)

        while self.departure not in path[self.destination]:
            for item in path[self.destination]:
                item_source = path[item]
                for subitem in item_source:
                    path[self.destination].append(subitem)

        shortest_path = path[self.destination]

        shortest_route: List = []
        for item in shortest_path:
            shortest_route.append((item, visited[item]))
        shortest_route.append((self.destination, visited[self.destination]))

        # sort shortest route by day in ascending order
        return sorted(shortest_route, key=lambda item: item[1])

    @staticmethod
    def _adjust_for_fuelling_needs(route: List, autonomy: int) -> List:
        new_route: List = []
        deviation: int = 0
        last_item = route[-1]
        fuel_budget: int = autonomy

        for i in range(len(route)):
            current_leg = route[i]
            new_route.append((current_leg[0], current_leg[1]+deviation))
            if current_leg != last_item:
                next_leg = route[i+1]
                next_flight_distance = next_leg[1] - current_leg[1]
                if next_flight_distance > fuel_budget:
                    deviation += 1
                    fuel_budget = autonomy
                    new_route.append((current_leg[0], current_leg[1]+deviation))
                fuel_budget = fuel_budget - next_flight_distance

        return new_route

    @staticmethod
    def _get_capture_attempt_count(shortest_path: List, hunter_schedule: Dict):
        capture_attempts: int = 0
        for stop in shortest_path:
            planet_name = stop[0]
            arrival_day = stop[1]
            if (
                    planet_name in hunter_schedule.keys()
                    and arrival_day in hunter_schedule[planet_name]
            ):
                capture_attempts += 1
        return capture_attempts

    @staticmethod
    def _convert_capture_probability_to_success_rate(probability_of_capture: float) -> int:
        """
        Converts the probability of capture to the success rate.
        :param probability_of_capture: the probability of capture (ranging from 0.0 to 1.0)
        :return: the success rate (ranging from 0 - 100)
        """
        probability_of_success: float = 1 - probability_of_capture
        return int(round(probability_of_success, 2) * 100)

    @staticmethod
    def _get_probability_of_capture(capture_attempt_count: int) -> float:
        """
        Calculates the probability of getting captured depending on the number of capture attempts.
        :param capture_attempt_count: number of capture attempts
        :return: the probability of getting captured
        """
        result: float = 0.0

        if capture_attempt_count == 0:
            return result

        for i in range(capture_attempt_count):
            result += (9 ** (i)) / (10 ** (i + 1))

        return result
