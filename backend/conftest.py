# import pytest
#
# from backend.converters import PlanetGraph
#
# TATOOINE = "Tatooine"
# DAGOBAH = "Dagobah"
# HOTH = "Hoth"
# ENDOR = "Endor"
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