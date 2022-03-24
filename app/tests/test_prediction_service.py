import pytest

from app.prediction_service import (
    Graph,
    get_probability_of_capture,
    get_probability_of_success,
    get_shortest_path_to_destination,
)

TATOOINE = "Tatooine"
DAGOBAH = "Dagobah"
HOTH = "Hoth"
ENDOR = "Endor"


@pytest.fixture
def planet_graph():
    planetGraph = Graph()

    planetGraph.add_node(TATOOINE)
    planetGraph.add_node(DAGOBAH)
    planetGraph.add_node(HOTH)
    planetGraph.add_node(ENDOR)

    planetGraph.add_edge(TATOOINE, DAGOBAH, 6)
    planetGraph.add_edge(ENDOR, DAGOBAH, 4)
    planetGraph.add_edge(HOTH, DAGOBAH, 1)
    planetGraph.add_edge(ENDOR, HOTH, 1)
    planetGraph.add_edge(HOTH, TATOOINE, 6)

    return planetGraph


def test_graph(planet_graph):
    assert planet_graph.edges == {
        TATOOINE: [DAGOBAH, HOTH],
        DAGOBAH: [TATOOINE, ENDOR, HOTH],
        ENDOR: [DAGOBAH, HOTH],
        HOTH: [DAGOBAH, ENDOR, TATOOINE],
    }
    assert planet_graph.nodes == {TATOOINE, DAGOBAH, ENDOR, HOTH}
    assert planet_graph.distances == {
        (TATOOINE, DAGOBAH): 6,
        (DAGOBAH, TATOOINE): 6,
        (DAGOBAH, ENDOR): 4,
        (ENDOR, DAGOBAH): 4,
        (DAGOBAH, HOTH): 1,
        (HOTH, DAGOBAH): 1,
        (HOTH, ENDOR): 1,
        (ENDOR, HOTH): 1,
        (TATOOINE, HOTH): 6,
        (HOTH, TATOOINE): 6,
    }


def test_s(planet_graph):
    autonomy: int = 6
    departure = TATOOINE
    destination = ENDOR

    expected_distance = 8
    expected_route = [HOTH, TATOOINE]
    expected_route = {
        TATOOINE: 0,
        HOTH: 6,
    }

    distance, route = get_shortest_path_to_destination(
        graph=planet_graph,
        departure=departure,
        destination=destination,
        autonomy=autonomy,
    )

    assert distance == expected_distance
    assert route == expected_route


def test_get_success_proba(planet_graph):
    autonomy: int = 6
    departure = TATOOINE
    destination = ENDOR
    countdown = 7
    expected = 0

    actual = get_probability_of_success(
        countdown=countdown,
        graph=planet_graph,
        departure=departure,
        destination=destination,
        autonomy=autonomy,
    )

    assert actual == expected


@pytest.fixture
def planet_graph2():
    planetGraph = Graph()

    planetGraph.add_node(TATOOINE)
    planetGraph.add_node(ENDOR)

    planetGraph.add_edge(TATOOINE, ENDOR, 6)

    return planetGraph


def test_algo2(planet_graph2):
    autonomy: int = 6
    departure = TATOOINE
    destination = ENDOR

    expected_distance = 6
    expected_route = [TATOOINE]

    distance = get_shortest_path_to_destination(
        graph=planet_graph2,
        departure=departure,
        destination=destination,
        autonomy=autonomy,
    )

    assert distance == expected_distance
    # assert route == expected_route


def test_get_probability_of_success2(planet_graph2):
    autonomy: int = 6
    departure = TATOOINE
    destination = ENDOR
    countdown = 7
    expected = 100

    actual = get_probability_of_success(
        countdown=countdown,
        graph=planet_graph2,
        departure=departure,
        destination=destination,
        autonomy=autonomy,
    )

    assert actual == expected


def test_get_probability_of_success3(planet_graph):
    autonomy: int = 6
    departure = TATOOINE
    destination = ENDOR
    countdown = 9
    expected = 100

    actual = get_probability_of_success(
        countdown=countdown,
        graph=planet_graph,
        departure=departure,
        destination=destination,
        autonomy=autonomy,
    )

    assert actual == expected


def test_get_probability_of_success4(planet_graph):
    autonomy: int = 6
    departure = TATOOINE
    destination = ENDOR
    countdown = 10
    expected = 100

    actual = get_probability_of_success(
        countdown=countdown,
        graph=planet_graph,
        departure=departure,
        destination=destination,
        autonomy=autonomy,
    )

    assert actual == expected


@pytest.fixture
def hunter_schedule():
    return {HOTH: {6, 7, 8}}


@pytest.mark.parametrize(
    "input,expected",
    [(1, 0.1), (2, 0.19), (3, 0.271), (0, 0)],
)
def test_get_probability_of_capture(input, expected):
    actual = get_probability_of_capture(input)

    assert actual == expected
