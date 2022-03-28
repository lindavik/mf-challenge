import pytest

from app.context import ContextLoader
from app.converters import MissionDetails, PlanetGraph
from tests.shared_test_utils import TATOOINE, DAGOBAH, ENDOR, HOTH


@pytest.fixture
def planet_graph():
    planet_graph: PlanetGraph = PlanetGraph()
    planet_graph.add_route(TATOOINE, DAGOBAH, 6)
    planet_graph.add_route(DAGOBAH, ENDOR, 4)
    planet_graph.add_route(DAGOBAH, HOTH, 1)
    planet_graph.add_route(HOTH, ENDOR, 1)
    planet_graph.add_route(TATOOINE, HOTH, 6)
    return planet_graph


def test_load_mission_details(planet_graph):
    file_path: str = "./sample_inputs/millennium-falcon.json"
    expected = MissionDetails(autonomy=6,
                              departure="Tatooine",
                              arrival="Endor",
                              routes=planet_graph)

    actual: MissionDetails = ContextLoader.load_mission_details(file_path=file_path)

    assert actual == expected
