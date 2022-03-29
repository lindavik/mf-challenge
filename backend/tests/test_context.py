# from backend.context import ContextLoader
# from backend.converters import MissionDetails, InterceptedData
#
# import pytest
#
# from backend.converters import PlanetGraph
#
# TATOOINE = "Tatooine"
# DAGOBAH = "Dagobah"
# HOTH = "Hoth"
# ENDOR = "Endor"
#
#
# @pytest.fixture(scope='session', autouse=True)
# def planet_graph(request):
#     planet_graph = PlanetGraph()
#     planet_graph.add_route(TATOOINE, DAGOBAH, 6)
#     planet_graph.add_route(ENDOR, DAGOBAH, 4)
#     planet_graph.add_route(HOTH, DAGOBAH, 1)
#     planet_graph.add_route(ENDOR, HOTH, 1)
#     planet_graph.add_route(HOTH, TATOOINE, 6)
#     return planet_graph
#
#
#
# def test_load_mission_details(planet_graph):
#     file_path: str = "./sample_inputs/millennium-falcon.json"
#     expected = MissionDetails(autonomy=6,
#                               departure=TATOOINE,
#                               arrival=ENDOR,
#                               routes=planet_graph)
#
#     actual: MissionDetails = ContextLoader.load_mission_details(file_path=file_path)
#
#     assert actual == expected
#
#
# def test_load_intercepted_data(planet_graph):
#     file_path: str = "./sample_inputs/empire.json"
#     expected_schedule = {
#         TATOOINE: {4},
#         DAGOBAH: {5}
#     }
#     expected = InterceptedData(countdown=6,
#                                bounty_hunter_schedule=expected_schedule)
#
#     actual: InterceptedData = ContextLoader.load_intercepted_data_from_file(file_path=file_path)
#
#     assert actual == expected
