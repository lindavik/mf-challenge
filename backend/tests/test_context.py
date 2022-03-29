from backend.src.context import ContextLoader
from backend.src.converters import MissionDetails, InterceptedData
from backend.tests.conftest import TATOOINE, ENDOR, DAGOBAH


def test_load_mission_details(planet_graph):
    file_path: str = "./sample_inputs/millennium-falcon.json"
    expected = MissionDetails(autonomy=6,
                              departure=TATOOINE,
                              arrival=ENDOR,
                              routes=planet_graph)

    actual: MissionDetails = ContextLoader.load_mission_details(file_path=file_path)

    assert actual == expected


def test_load_intercepted_data(planet_graph):
    file_path: str = "./sample_inputs/empire.json"
    expected_schedule = {
        TATOOINE: {4},
        DAGOBAH: {5}
    }
    expected = InterceptedData(countdown=6,
                               bounty_hunter_schedule=expected_schedule)

    actual: InterceptedData = ContextLoader.load_intercepted_data_from_file(file_path=file_path)

    assert actual == expected
