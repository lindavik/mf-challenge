from collections import defaultdict
from typing import Dict

from app.converters import PlanetGraph


class PredictionService(object):
    def __init__(self):
       pass

    def get_probability_of_success(self):
        pass


def get_probability_of_success(
    countdown, graph, departure, destination, autonomy, hunter_schedule
) -> int:
    """
    Calculates the probability of success, returns a number ranging from 0 to 100.
    :param countdown:
    :param graph:
    :param departure:
    :param destination:
    :param autonomy:
    :return: the probability of success (ranging from 0 - 100)
    """
    shortest_path = _get_shortest_path_to_destination(
        graph, departure, destination, autonomy
    )
    earliest_arrival_day = shortest_path[destination]
    if earliest_arrival_day > countdown:
        return 0
    else:
        # travel_budget = countdown - shortest_path
        capture_attempt_count = _get_capture_attempt_count(
            shortest_path=shortest_path, hunter_schedule=hunter_schedule
        )

        probability_of_capture: float = _get_probability_of_capture(
            capture_attempt_count=capture_attempt_count
        )
        return _convert_capture_probability_to_success_rate(
            probability_of_capture=probability_of_capture
        )


def _get_shortest_path_to_destination(
    planet_graph: PlanetGraph, departure: str, destination: str, autonomy: int
):
    """
    Determines the shortest path from the departure planet to the destination planet.
    Disclaimer: provides with only one route, if there are two equally long shortest routes, only one will be returned.
    :param planet_graph:
    :param departure:
    :param destination:
    :param autonomy:
    :return:
    """
    visited = {departure: 0}
    path = defaultdict(list)
    nodes = set(planet_graph.planets)

    while nodes:
        minNode = None
        for node in nodes:
            if node in visited:
                if minNode is None:
                    minNode = node
                elif visited[node] < visited[minNode]:
                    minNode = node
        if minNode is None:
            break

        nodes.remove(minNode)
        current_distance_travelled = visited[minNode]

        for edge in planet_graph.routes[minNode]:

            new_distance = (
                current_distance_travelled + planet_graph.distances[(minNode, edge)]
            )

            #todo fix: incorrect logic
            if new_distance > autonomy:
                new_distance += 1

            if edge not in visited or new_distance < visited[edge]:
                visited[edge] = new_distance
                path[edge] = []
                path[edge].append(minNode)

    while departure not in path[destination]:
        for item in path[destination]:
            item_source = path[item]
            for subitem in item_source:
                path[destination].append(subitem)

    shortest_path = path[destination]

    earliest_arrival_map = {}
    for item in shortest_path:
        earliest_arrival_map[item] = visited[item]
    earliest_arrival_map[destination] = visited[destination]

    return earliest_arrival_map


def _convert_capture_probability_to_success_rate(probability_of_capture: float) -> int:
    """
    Converts the probability of capture to the success rate.
    :param probability_of_capture: the probability of capture (ranging from 0.0 to 1.0)
    :return: the success rate (ranging from 0 - 100)
    """
    probability_of_success: float = 1 - probability_of_capture
    return int(round(probability_of_success, 2) * 100)


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


def _get_capture_attempt_count(shortest_path: Dict, hunter_schedule: Dict):
    capture_attempts: int = 0
    for planet in shortest_path.items():
        planet_name = planet[0]
        arrival_day = planet[1]
        if (
            planet_name in hunter_schedule.keys()
            and arrival_day in hunter_schedule[planet_name]
        ):
            capture_attempts += 1
    return capture_attempts
