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


def dijkstra(graph, initial):
    visited = {initial: 0}
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
        currentWeight = visited[minNode]

        for edge in graph.edges[minNode]:
            weight = currentWeight + graph.distances[(minNode, edge)]
            if edge not in visited or weight < visited[edge]:
                visited[edge] = weight
                path[edge].append(minNode)

    return visited, path


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
            weight = current_distance_travelled + graph.distances[(minNode, edge)]
            if edge not in visited or weight < visited[edge]:
                visited[edge] = weight
                path[edge].append(minNode)

    return visited[destination], path


# print(dijkstra(customGraph, "A"))
# algo(planetGraph, TATOOINE, ENDOR)
