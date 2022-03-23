from collections import defaultdict


class Graph:
    def __init__(self):
        self.nodes = set()
        self.edges = defaultdict(list)
        self.distances = {}

    def add_node(self, value):
        self.nodes.add(value)

    def add_edge(self, fromNode, toNode, distance):
        self.edges[fromNode].append(toNode)
        self.edges[toNode].append(fromNode)

        self.distances[(fromNode, toNode)] = distance
        self.distances[(toNode, fromNode)] = distance


def algo(graph, departure, destination, autonomy: int):

    visited = {departure: 0}
    path = defaultdict(list)
    nodes = set(graph.nodes)

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

        for edge in graph.edges[minNode]:

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

    print("Path: " + str(path[destination]))
    return visited[destination]


def get_success_proba(countdown, graph, departure, destination, autonomy):
    shortest_path = algo(graph, departure, destination, autonomy)
    if shortest_path > countdown:
        return 0
    else:
        return 100


def calculate_proba(capture_attempt_count: int):
    result = 0

    if capture_attempt_count == 0:
        return result

    for i in range(capture_attempt_count):
        result += (9 ** (i)) / (10 ** (i + 1))

    return result
