from typing import List

import pytest
from givemetheodds.converters import MissionDetails, PlanetGraph
from givemetheodds.prediction_service import PredictionService

TATOOINE = "Tatooine"
DAGOBAH = "Dagobah"
HOTH = "Hoth"
ENDOR = "Endor"


@pytest.fixture(scope="session", autouse=True)
def planet_graph(request):
    planet_graph = PlanetGraph()
    planet_graph.add_route(TATOOINE, DAGOBAH, 6)
    planet_graph.add_route(ENDOR, DAGOBAH, 4)
    planet_graph.add_route(HOTH, DAGOBAH, 1)
    planet_graph.add_route(ENDOR, HOTH, 1)
    planet_graph.add_route(HOTH, TATOOINE, 6)
    return planet_graph


@pytest.fixture
def prediction_service(planet_graph):
    mission_details: MissionDetails = MissionDetails(
        autonomy=6, arrival=ENDOR, departure=TATOOINE, routes=planet_graph
    )
    return PredictionService(mission_details=mission_details)


@pytest.mark.parametrize(
    "input_countdown, expected",
    [
        (9, [["Tatooine", "Dagobah", "Hoth", "Endor"], ["Tatooine", "Hoth", "Endor"]]),
        (8, [["Tatooine", "Hoth", "Endor"]]),
        (7, []),
    ],
)
def test__get_all_paths_between_two_nodes(
    prediction_service, input_countdown, expected
):
    prediction_service._generate_all_paths_between_two_planets(
        TATOOINE, ENDOR, input_countdown
    )

    assert prediction_service.paths == expected


@pytest.fixture
def planet_graph_minimal():
    planet_graph = PlanetGraph()
    planet_graph.add_route(TATOOINE, ENDOR, 6)
    return planet_graph


def test__adjust_for_fuelling_needs_multiple():
    autonomy: int = 6
    route: List = [(TATOOINE, 0), ("Random", 3), (HOTH, 7), (ENDOR, 12)]
    expected: List = [
        (TATOOINE, 0),
        ("Random", 3),
        ("Random", 4),
        (HOTH, 8),
        (HOTH, 9),
        (ENDOR, 14),
    ]

    actual = PredictionService._adjust_for_fuelling_needs(
        route=route, autonomy=autonomy
    )

    assert actual == expected


@pytest.mark.parametrize(
    "input_countdown, expected",
    [(10, 100), (9, 90), (8, 81), (7, 0), (6, 0), (4, 0)],
)
def test_get_probability_of_success(
    prediction_service, input_countdown, expected, hunter_schedule_set
):
    actual = prediction_service.get_probability_of_success(
        countdown=input_countdown,
        hunter_schedule=hunter_schedule_set,
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


def test__get_capture_attempt_count_with_capture(hunter_schedule_set):
    shortest_path: List = [(TATOOINE, 0), (HOTH, 7), (ENDOR, 9)]
    expected: int = 1

    actual = PredictionService._get_capture_attempt_count(
        route=shortest_path, hunter_schedule=hunter_schedule_set
    )

    assert actual == expected


def test__get_capture_attempt_count_without_capture():
    hunter_schedule = [(TATOOINE, 6), (TATOOINE, 7), (TATOOINE, 8)]
    shortest_path = [(TATOOINE, 0), (HOTH, 7), (ENDOR, 9)]
    expected: int = 0

    actual = PredictionService._get_capture_attempt_count(
        route=shortest_path, hunter_schedule=hunter_schedule
    )

    assert actual == expected


def test__get_travel_in_days(prediction_service):
    route = ["Tatooine", "Hoth", "Endor"]
    expected = 8

    actual = prediction_service._get_travel_in_days(route)

    assert expected == actual


@pytest.mark.parametrize(
    "input_path, expected",
    [
        (
            ["Tatooine", "Dagobah", "Hoth", "Endor"],
            [
                ("Tatooine", 0),
                ("Dagobah", 6),
                ("Dagobah", 7),
                ("Hoth", 8),
                ("Endor", 9),
            ],
        ),
        (
            ["Tatooine", "Hoth", "Endor"],
            [("Tatooine", 0), ("Hoth", 6), ("Hoth", 7), ("Endor", 8)],
        ),
    ],
)
def test__get_detailed_travel_plan(input_path, expected, prediction_service):
    actual = prediction_service._get_detailed_travel_plan(input_path)

    assert actual == expected


@pytest.fixture
def hunter_schedule_set():
    return {(HOTH, 6), (HOTH, 7), (HOTH, 8)}


def test__can_avoid_bounty_hunters_set1(hunter_schedule_set):
    delay_budget = 2
    stop = (TATOOINE, 0)
    expected = True

    actual = PredictionService._can_avoid_bounty_hunters_set(
        stop, delay_budget=delay_budget, hunter_schedule=hunter_schedule_set
    )

    assert actual == expected


def test__can_avoid_bounty_hunters_set2(hunter_schedule_set):
    delay_budget = 2
    stop = (HOTH, 6)
    expected = False

    actual = PredictionService._can_avoid_bounty_hunters_set(
        stop, delay_budget=delay_budget, hunter_schedule=hunter_schedule_set
    )

    assert actual == expected


def test__optimize_path_v1(hunter_schedule_set):
    countdown: int = 10
    path = [("Tatooine", 0), ("Hoth", 6), ("Hoth", 7), ("Endor", 8)]
    expected = [("Tatooine", 0), ("Hoth", 6), ("Hoth", 7), ("Endor", 8)]

    actual = PredictionService._optimize_path(
        path, hunter_schedule=hunter_schedule_set, countdown=countdown
    )

    assert actual == expected


def test__optimize_path_v2(hunter_schedule_set):
    countdown: int = 11
    path = [("Tatooine", 0), ("Dagobah", 6), ("Dagobah", 7), ("Hoth", 8), ("Endor", 9)]
    expected = [
        ("Tatooine", 0),
        ("Dagobah", 6),
        ("Dagobah", 7),
        ("Dagobah", 8),
        ("Hoth", 9),
        ("Endor", 10),
    ]

    actual = PredictionService._optimize_path(
        path, hunter_schedule=hunter_schedule_set, countdown=countdown
    )

    assert actual == expected


def test__get_lowest_capture_count(hunter_schedule_set):
    optimized_paths: List = [
        [
            ("Tatooine", 0),
            ("Dagobah", 6),
            ("Dagobah", 7),
            ("Dagobah", 8),
            ("Hoth", 9),
            ("Endor", 10),
        ],
        [("Tatooine", 0), ("Hoth", 6), ("Hoth", 7), ("Endor", 8)],
    ]
    expected = 0

    actual = PredictionService._get_lowest_capture_count(
        hunter_schedule=hunter_schedule_set, optimized_paths=optimized_paths
    )

    assert actual == expected
