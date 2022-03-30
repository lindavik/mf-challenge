import os

import pytest

from givemetheodds.context import ContextLoader
from givemetheodds.converters import MissionDetails, InterceptedData, PlanetGraph

TATOOINE = "Tatooine"
DAGOBAH = "Dagobah"
HOTH = "Hoth"
ENDOR = "Endor"


@pytest.fixture
def planet_graph():
    planet_graph = PlanetGraph()
    planet_graph.add_route(TATOOINE, DAGOBAH, 6)
    planet_graph.add_route(ENDOR, DAGOBAH, 4)
    planet_graph.add_route(HOTH, DAGOBAH, 1)
    planet_graph.add_route(ENDOR, HOTH, 1)
    planet_graph.add_route(HOTH, TATOOINE, 6)
    return planet_graph


@pytest.fixture
def current_file_path():
    return os.path.dirname(os.path.realpath(__file__))


def test_load_mission_details(current_file_path, planet_graph):
    file_path: str = os.path.join(current_file_path, "sample_inputs/millennium-falcon.json")

    expected: MissionDetails = MissionDetails(autonomy=6,
                              departure=TATOOINE,
                              arrival=ENDOR,
                              routes=planet_graph)

    actual: MissionDetails = ContextLoader.load_mission_details(file_path=file_path)

    assert actual.routes == expected.routes


def test_load_intercepted_data(current_file_path, planet_graph):
    file_path: str = os.path.join(current_file_path, "sample_inputs/empire.json")
    expected_schedule = {
        TATOOINE: {4},
        DAGOBAH: {5}
    }
    expected = InterceptedData(countdown=6,
                               bounty_hunter_schedule=expected_schedule)

    actual: InterceptedData = ContextLoader.load_intercepted_data_from_file(file_path=file_path)

    assert actual == expected
