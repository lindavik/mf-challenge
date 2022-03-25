from collections import defaultdict


class PlanetGraph:
    def __init__(self):
        self.planets = set()
        self.routes = defaultdict(list)
        self.distances = {}

    def add_planet(self, planet_name: str):
        self.planets.add(planet_name)

    def add_route(self, departure_planet: str, destination_planet: str, distance: int):
        self.routes[departure_planet].append(destination_planet)
        self.routes[destination_planet].append(departure_planet)
        self.distances[(departure_planet, destination_planet)] = distance
        self.distances[(destination_planet, departure_planet)] = distance


def get_shortest_path_to_destination(graph, departure, destination, autonomy: int):
    visited = {departure: 0}
    path = defaultdict(list)
    nodes = set(graph.planets)

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

        for edge in graph.routes[minNode]:

            new_distance = current_distance_travelled + graph.distances[(minNode, edge)]

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

    earliest_arrival_map = {}
    for item in path[destination]:
        earliest_arrival_map[item] = visited[item]

    print("Path: " + str(path[destination]))
    return visited[destination], earliest_arrival_map


def get_probability_of_success(
    countdown, graph, departure, destination, autonomy
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
    shortest_path = get_shortest_path_to_destination(
        graph, departure, destination, autonomy
    )
    if shortest_path > countdown:
        return 0
    else:
        # travel_budget = countdown - shortest_path
        capture_attempt_count = 0
        probability_of_capture: float = get_probability_of_capture(
            capture_attempt_count=capture_attempt_count
        )
        return convert_capture_probability_to_success_rate(
            probability_of_capture=probability_of_capture
        )


def convert_capture_probability_to_success_rate(probability_of_capture: float) -> int:
    """
    Converts the probability of capture to the success rate.
    :param probability_of_capture: the probability of capture (ranging from 0.0 to 1.0)
    :return: the success rate (ranging from 0 - 100)
    """
    probability_of_success: float = 1 - probability_of_capture
    return int(round(probability_of_success, 2) * 100)


def get_probability_of_capture(capture_attempt_count: int) -> float:
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