# from typing import Dict
#
# import pytest
#
# from backend.converters import MissionDetails, MissionConverter, InterceptedData, InterceptedDataConverter
#
# TATOOINE = "Tatooine"
# DAGOBAH = "Dagobah"
# HOTH = "Hoth"
# ENDOR = "Endor"
#
#
# def test_get_mission_details(planet_graph):
#     details: Dict = {
#         "autonomy": 6,
#         "departure": "Tatooine",
#         "arrival": "Endor",
#         "routes_db": "universe.db"
#     }
#     directory: str = "sample_inputs/"
#     expected: MissionDetails = MissionDetails(autonomy=6,
#                                               departure="Tatooine",
#                                               arrival="Endor",
#                                               routes=planet_graph)
#
#     actual: MissionDetails = MissionConverter.map_to_mission_details(details, directory=directory)
#
#     assert actual == expected
#
#
# def test_get_mission_details_bad_field_format():
#     directory: str = "sample_inputs/"
#     details: Dict = {
#         "autonomy": "6",
#         "departure": "Tatooine",
#         "arrival": "Endor",
#         "routes_db": "universe.db"
#     }
#     with pytest.raises(Exception):
#         MissionConverter.map_to_mission_details(details, directory)
#
#
# def test_get_mission_details_with_unknown_fields(planet_graph):
#     directory: str = "sample_inputs/"
#     details: Dict = {
#         "autonomy": 6,
#         "departure": "Tatooine",
#         "arrival": "Endor",
#         "routes_db": "universe.db",
#         "should_not_be_here": "nope"
#     }
#
#     expected: MissionDetails = MissionDetails(autonomy=6,
#                                               departure="Tatooine",
#                                               arrival="Endor",
#                                               routes=planet_graph)
#
#     actual: MissionDetails = MissionConverter.map_to_mission_details(details, directory)
#
#     assert actual == expected
#
#
# def test_get_mission_details_missing_required_details():
#     directory: str = "sample_inputs/"
#     with pytest.raises(Exception):
#         details = {
#             "autonomy": 6,
#             "arrival": "Endor",
#             "routes_db": "universe.db"
#         }
#         MissionConverter.map_to_mission_details(details, directory)
#
#
# def test_get_mission_details_invalid_autonomy():
#     directory: str = "sample_inputs/"
#     with pytest.raises(Exception):
#         details = {
#             "autonomy": -6,
#             "arrival": "Endor",
#             "departure": "Tatooine",
#             "routes_db": "universe.db"
#         }
#         MissionConverter.map_to_mission_details(details, directory)
#
#
# def test_planet_graph(planet_graph):
#     assert planet_graph.routes == {
#         TATOOINE: [DAGOBAH, HOTH],
#         DAGOBAH: [TATOOINE, ENDOR, HOTH],
#         ENDOR: [DAGOBAH, HOTH],
#         HOTH: [DAGOBAH, ENDOR, TATOOINE],
#     }
#     assert planet_graph.planets == {TATOOINE, DAGOBAH, ENDOR, HOTH}
#     assert planet_graph.distances == {
#         (TATOOINE, DAGOBAH): 6,
#         (DAGOBAH, TATOOINE): 6,
#         (DAGOBAH, ENDOR): 4,
#         (ENDOR, DAGOBAH): 4,
#         (DAGOBAH, HOTH): 1,
#         (HOTH, DAGOBAH): 1,
#         (HOTH, ENDOR): 1,
#         (ENDOR, HOTH): 1,
#         (TATOOINE, HOTH): 6,
#         (HOTH, TATOOINE): 6,
#     }
#
#
# def test_map_to_intercepted_data():
#     bounty_hunter_schedule = {
#         HOTH: {6, 7, 8},
#         ENDOR: {9}
#     }
#     raw_data = {
#         "countdown": 7,
#         "bounty_hunters": [
#             {"planet": "Hoth", "day": 6},
#             {"planet": "Hoth", "day": 7},
#             {"planet": "Hoth", "day": 8},
#             {"planet": "Endor", "day": 9}
#         ]
#     }
#     expected = InterceptedData(countdown=7, bounty_hunter_schedule=bounty_hunter_schedule)
#
#     actual = InterceptedDataConverter.map_to_intercepted_data(raw_data=raw_data)
#
#     assert actual == expected
#
#
# def test_process_schedule():
#     raw_schedule = [
#         {"planet": "Hoth", "day": 6},
#         {"planet": "Hoth", "day": 7},
#         {"planet": "Hoth", "day": 8},
#         {"planet": "Endor", "day": 9}
#     ]
#     expected = {
#         HOTH: {6, 7, 8},
#         ENDOR: {9}
#     }
#
#     actual = InterceptedDataConverter._process_schedule(raw_schedule=raw_schedule)
#
#     assert actual == expected
