from typing import List

import pytest

from givemetheodds.converters import MissionDetails
from givemetheodds.converters import PlanetGraph
from givemetheodds.prediction_service import PredictionService

TATOOINE = "Tatooine"
DAGOBAH = "Dagobah"
HOTH = "Hoth"
ENDOR = "Endor"


@pytest.fixture(scope='session', autouse=True)
def planet_graph(request):
    planet_graph = PlanetGraph()
    planet_graph.add_route(TATOOINE, DAGOBAH, 6)
    planet_graph.add_route(ENDOR, DAGOBAH, 4)
    planet_graph.add_route(HOTH, DAGOBAH, 1)
    planet_graph.add_route(ENDOR, HOTH, 1)
    planet_graph.add_route(HOTH, TATOOINE, 6)
    return planet_graph


@pytest.fixture
def hunter_schedule():
    return {HOTH: {6, 7, 8}}


@pytest.fixture
def prediction_service(planet_graph):
    mission_details: MissionDetails = MissionDetails(autonomy=6,
                                                     arrival=ENDOR,
                                                     departure=TATOOINE,
                                                     routes=planet_graph)
    return PredictionService(mission_details=mission_details)


def test_get_shortest_path_to_destination(prediction_service):
    expected_route = [('Tatooine', 0), ('Hoth', 6), ('Endor', 7)]

    route = prediction_service._get_shortest_path_to_destination()

    assert route == expected_route


def test__adjust_for_fuelling_needs():
    autonomy: int = 6
    route = [('Tatooine', 0), ('Hoth', 6), ('Endor', 7)]
    expected = [('Tatooine', 0), ('Hoth', 6), ('Hoth', 7), ('Endor', 8)]

    actual = PredictionService._adjust_for_fuelling_needs(route=route, autonomy=autonomy)

    assert actual == expected


def test__adjust_for_fuelling_needs_multiple_refuellings():
    autonomy: int = 6
    route: List = [('Tatooine', 0), ('Random', 3), ('Hoth', 7), ('Endor', 12)]
    expected: List = [('Tatooine', 0), ('Random', 3), ('Random', 4), ('Hoth', 8), ('Hoth', 9), ('Endor', 14)]

    actual = PredictionService._adjust_for_fuelling_needs(route=route, autonomy=autonomy)

    assert actual == expected


@pytest.fixture
def planet_graph_minimal():
    planet_graph = PlanetGraph()
    planet_graph.add_route(TATOOINE, ENDOR, 6)
    return planet_graph


def test_get_shortest_path_to_destination_minimal(planet_graph_minimal):
    mission_details: MissionDetails = MissionDetails(autonomy=6,
                                                     arrival=ENDOR,
                                                     departure=TATOOINE,
                                                     routes=planet_graph_minimal)
    prediction_service = PredictionService(mission_details=mission_details)

    expected_route = [(TATOOINE, 0), (ENDOR, 6)]

    route = prediction_service._get_shortest_path_to_destination()

    assert route == expected_route


@pytest.mark.parametrize(
    "countdown, expected",
    [
        (10, 100),
        # (9, 90),
        # (8, 81),
        # (7, 0),
        # (6, 0)
    ],
)
def test_get_probability_of_success(prediction_service, countdown, expected, hunter_schedule
                                    ):
    actual = prediction_service.get_probability_of_success(
        countdown=countdown,
        hunter_schedule=hunter_schedule,
    )

    assert actual == expected


@pytest.mark.parametrize(
    "input,expected",
    [(1, 0.1), (2, 0.19), (3, 0.271), (0, 0)],
)
def test_get_probability_of_capture(input, expected):
    actual = PredictionService._get_probability_of_capture(input)

    assert actual == expected


@pytest.mark.parametrize(
    "input,expected",
    [(0.231, 77), (0, 100), (1.0, 0), (0.19, 81), (0.11789, 88)],
)
def test_convert_capture_probability_to_success_rate(input, expected):
    actual = PredictionService._convert_capture_probability_to_success_rate(input)

    assert actual == expected


def test__get_capture_attempt_count_with_capture(hunter_schedule):
    shortest_path: List = [(TATOOINE, 0), (HOTH, 7), (ENDOR, 9)]
    expected: int = 1

    actual = PredictionService._get_capture_attempt_count(
        shortest_path=shortest_path, hunter_schedule=hunter_schedule
    )

    assert actual == expected


def test__get_capture_attempt_count_without_capture():
    hunter_schedule = {TATOOINE: {6, 7, 8}}
    shortest_path = [(TATOOINE, 0), (HOTH, 7), (ENDOR, 9)]
    expected: int = 0

    actual = PredictionService._get_capture_attempt_count(
        shortest_path=shortest_path, hunter_schedule=hunter_schedule
    )

    assert actual == expected


def test__get_lowest_capture_attempt_count_with_no_delay_budget(hunter_schedule):
    shortest_path: List = [(TATOOINE, 0), (HOTH, 7), (ENDOR, 9)]
    expected: int = 1
    delay_budget: int = 0

    actual = PredictionService._get_lowest_capture_attempt_count(shortest_path=shortest_path,
                                                                 hunter_schedule=hunter_schedule,
                                                                 delay_budget=delay_budget)

    assert actual == expected


def test__get_lowest_capture_attempt_count_with_delay_budget():
    hunter_schedule = {
        HOTH: {7},
        ENDOR: {9}
    }
    shortest_path: List = [(TATOOINE, 0), (HOTH, 7), (ENDOR, 9)]
    expected: int = 0
    delay_budget: int = 2

    actual = PredictionService._get_lowest_capture_attempt_count(shortest_path=shortest_path,
                                                                 hunter_schedule=hunter_schedule,
                                                                 delay_budget=delay_budget)

    assert actual == expected


def test___add_wait_at_index_0():
    index: int = 0
    route: List = [('Tatooine', 0), ('Random', 3), ('Random', 4), ('Hoth', 8), ('Hoth', 9), ('Endor', 14)]
    expected: List = [('Tatooine', 0), ('Tatooine', 1), ('Random', 4), ('Random', 5), ('Hoth', 9), ('Hoth', 10),
                      ('Endor', 15)]

    actual = PredictionService._add_wait_at_index(route=route, index=index)

    assert actual == expected


def test___add_wait_at_index_0_v2():
    index: int = 0
    route: List = [('Tatooine', 0), ('Hoth', 7), ('Endor', 8)]
    expected: List = [('Tatooine', 0), ('Tatooine', 1), ('Hoth', 8), ('Endor', 9)]

    actual = PredictionService._add_wait_at_index(route=route, index=index)

    assert actual == expected


def test___add_wait_at_index_2():
    index: int = 2
    route: List = [('Tatooine', 0), ('Random', 3), ('Random', 4), ('Hoth', 8), ('Hoth', 9), ('Endor', 14)]
    expected: List = [('Tatooine', 0), ('Random', 3), ('Random', 4), ('Random', 5), ('Hoth', 9), ('Hoth', 10),
                      ('Endor', 15)]

    actual = PredictionService._add_wait_at_index(route=route, index=index)

    assert actual == expected
