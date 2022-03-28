import pytest

from app.prediction_service import (
    PlanetGraph,
    _convert_capture_probability_to_success_rate,
    _get_capture_attempt_count,
    _get_probability_of_capture,
    get_probability_of_success,
    _get_shortest_path_to_destination,
)
from tests.shared_test_utils import HOTH, TATOOINE, ENDOR, planet_graph, DAGOBAH


@pytest.fixture
def hunter_schedule():
    return {HOTH: {6, 7, 8}}


def test_get_shortest_path_to_destination_extended(planet_graph):
    autonomy: int = 6
    departure = TATOOINE
    destination = ENDOR

    expected_route = {TATOOINE: 0, HOTH: 6, ENDOR: 8}

    route = _get_shortest_path_to_destination(
        planet_graph=planet_graph,
        departure=departure,
        destination=destination,
        autonomy=autonomy,
    )

    assert route == expected_route


def test_get_probability_of_success(planet_graph_extended, hunter_schedule):
    autonomy: int = 6
    departure = TATOOINE
    destination = ENDOR
    countdown = 7
    expected = 0

    actual = get_probability_of_success(
        countdown=countdown,
        graph=planet_graph_extended,
        departure=departure,
        destination=destination,
        autonomy=autonomy,
        hunter_schedule=hunter_schedule,
    )

    assert actual == expected


@pytest.fixture
def planet_graph_minimal():
    planet_graph = PlanetGraph()
    planet_graph.add_planet(TATOOINE)
    planet_graph.add_planet(ENDOR)
    planet_graph.add_route(TATOOINE, ENDOR, 6)
    return planet_graph


def test_get_shortest_path_to_destination_minimal(planet_graph_minimal):
    autonomy: int = 6
    departure = TATOOINE
    destination = ENDOR

    expected_route = {TATOOINE: 0, ENDOR: 6}

    route = _get_shortest_path_to_destination(
        planet_graph=planet_graph_minimal,
        departure=departure,
        destination=destination,
        autonomy=autonomy,
    )

    assert route == expected_route


@pytest.mark.parametrize(
    "input_countdown, expected",
    [(10, 90), (9, 90), (7, 0), (6, 0)],
)
def test_get_probability_of_success(
    planet_graph, input_countdown, expected, hunter_schedule
):
    autonomy: int = 6
    departure = TATOOINE
    destination = ENDOR

    actual = get_probability_of_success(
        countdown=input_countdown,
        graph=planet_graph,
        departure=departure,
        destination=destination,
        autonomy=autonomy,
        hunter_schedule=hunter_schedule,
    )

    assert actual == expected


@pytest.mark.parametrize(
    "input,expected",
    [(1, 0.1), (2, 0.19), (3, 0.271), (0, 0)],
)
def test_get_probability_of_capture(input, expected):
    actual = _get_probability_of_capture(input)

    assert actual == expected


@pytest.mark.parametrize(
    "input,expected",
    [(0.231, 77), (0, 100), (1.0, 0), (0.19, 81), (0.11789, 88)],
)
def test_convert_capture_probability_to_success_rate(input, expected):
    actual = _convert_capture_probability_to_success_rate(input)

    assert actual == expected


def test__get_capture_attempt_count_with_capture(hunter_schedule):
    shortest_path = {TATOOINE: 0, HOTH: 7, ENDOR: 9}
    expected: int = 1

    actual = _get_capture_attempt_count(
        shortest_path=shortest_path, hunter_schedule=hunter_schedule
    )

    assert actual == expected


def test__get_capture_attempt_count_without_capture():
    hunter_schedule = {TATOOINE: {6, 7, 8}}
    shortest_path = {TATOOINE: 0, HOTH: 7, ENDOR: 9}
    expected: int = 0

    actual = _get_capture_attempt_count(
        shortest_path=shortest_path, hunter_schedule=hunter_schedule
    )

    assert actual == expected


# @pytest.fixture
# def planet_graph_extended_v2():
#     planet_graph = PlanetGraph()
#
#     planet_graph.add_planet(TATOOINE)
#     planet_graph.add_planet(DAGOBAH)
#     planet_graph.add_planet(HOTH)
#     planet_graph.add_planet(ENDOR)
#
#     planet_graph.add_route(TATOOINE, DAGOBAH,6)
#     planet_graph.add_route(DAGOBAH, HOTH, 4)
#     planet_graph.add_route(HOTH, ENDOR, 2)
#
#     return planet_graph


# def test_get_shortest_path_to_destination_extended_v2(planet_graph_extended_v2):
#     autonomy: int = 6
#     departure = TATOOINE
#     destination = ENDOR
#
#     expected_route = {TATOOINE: 0, DAGOBAH: 6, HOTH: 11, ENDOR: 13}
#
#     route = get_shortest_path_to_destination(
#         planet_graph=planet_graph_extended_v2,
#         departure=departure,
#         destination=destination,
#         autonomy=autonomy,
#     )
#
#     assert route == expected_route

