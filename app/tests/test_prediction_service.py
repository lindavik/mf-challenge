import pytest

from app.prediction_service import Graph, algo, calculate_proba, get_success_proba

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
        "Tatooine": ["Dagobah", "Hoth"],
        "Dagobah": ["Tatooine", "Endor", "Hoth"],
        "Endor": ["Dagobah", "Hoth"],
        "Hoth": ["Dagobah", "Endor", "Tatooine"],
    }
    assert planet_graph.nodes == {"Tatooine", "Dagobah", "Endor", "Hoth"}
    assert planet_graph.distances == {
        ("Tatooine", "Dagobah"): 6,
        ("Dagobah", "Tatooine"): 6,
        ("Dagobah", "Endor"): 4,
        ("Endor", "Dagobah"): 4,
        ("Dagobah", "Hoth"): 1,
        ("Hoth", "Dagobah"): 1,
        ("Hoth", "Endor"): 1,
        ("Endor", "Hoth"): 1,
        ("Tatooine", "Hoth"): 6,
        ("Hoth", "Tatooine"): 6,
    }


def test_algo(planet_graph):
    autonomy: int = 6
    departure = TATOOINE
    destination = ENDOR

    expected_distance = 8
    expected_route = [HOTH, TATOOINE]

    distance, route = algo(
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

    actual = get_success_proba(
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

    distance, route = algo(
        graph=planet_graph2,
        departure=departure,
        destination=destination,
        autonomy=autonomy,
    )

    assert distance == expected_distance
    assert route == expected_route


def test_get_success_proba2(planet_graph2):
    autonomy: int = 6
    departure = TATOOINE
    destination = ENDOR
    countdown = 7
    expected = 100

    actual = get_success_proba(
        countdown=countdown,
        graph=planet_graph2,
        departure=departure,
        destination=destination,
        autonomy=autonomy,
    )

    assert actual == expected


def test_get_success_proba3(planet_graph):
    autonomy: int = 6
    departure = TATOOINE
    destination = ENDOR
    countdown = 9
    expected = 100

    actual = get_success_proba(
        countdown=countdown,
        graph=planet_graph,
        departure=departure,
        destination=destination,
        autonomy=autonomy,
    )

    assert actual == expected


def test_get_success_proba4(planet_graph):
    autonomy: int = 6
    departure = TATOOINE
    destination = ENDOR
    countdown = 10
    expected = 100

    actual = get_success_proba(
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
def test_calculate_proba(input, expected):
    actual = calculate_proba(input)

    assert actual == expected
