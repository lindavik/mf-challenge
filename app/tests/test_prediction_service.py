import pytest

from app.prediction_service import (
    PlanetGraph,
    convert_capture_probability_to_success_rate,
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
    planetGraph = PlanetGraph()

    planetGraph.add_planet(TATOOINE)
    planetGraph.add_planet(DAGOBAH)
    planetGraph.add_planet(HOTH)
    planetGraph.add_planet(ENDOR)

    planetGraph.add_route(TATOOINE, DAGOBAH, 6)
    planetGraph.add_route(ENDOR, DAGOBAH, 4)
    planetGraph.add_route(HOTH, DAGOBAH, 1)
    planetGraph.add_route(ENDOR, HOTH, 1)
    planetGraph.add_route(HOTH, TATOOINE, 6)

    return planetGraph


def test_planet_graph(planet_graph):
    assert planet_graph.routes == {
        TATOOINE: [DAGOBAH, HOTH],
        DAGOBAH: [TATOOINE, ENDOR, HOTH],
        ENDOR: [DAGOBAH, HOTH],
        HOTH: [DAGOBAH, ENDOR, TATOOINE],
    }
    assert planet_graph.planets == {TATOOINE, DAGOBAH, ENDOR, HOTH}
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


def test_get_shortest_path_to_destination(planet_graph):
    autonomy: int = 6
    departure = TATOOINE
    destination = ENDOR

    expected_distance = 8
    expected_route = {
        TATOOINE: 0,
        HOTH: 6,
    }

    distance, route = get_shortest_path_to_destination(
        planet_graph=planet_graph,
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
    planetGraph = PlanetGraph()

    planetGraph.add_planet(TATOOINE)
    planetGraph.add_planet(ENDOR)

    planetGraph.add_route(TATOOINE, ENDOR, 6)

    return planetGraph


def test_algo2(planet_graph2):
    autonomy: int = 6
    departure = TATOOINE
    destination = ENDOR

    expected_distance = 6
    expected_route = [TATOOINE]

    distance = get_shortest_path_to_destination(
        planet_graph=planet_graph2,
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


@pytest.mark.parametrize(
    "input,expected",
    [(0.231, 77), (0, 100), (1.0, 0), (0.19, 81), (0.11789, 88)],
)
def test_convert_capture_probability_to_success_rate(input, expected):
    actual = convert_capture_probability_to_success_rate(input)

    assert actual == expected
