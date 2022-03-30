import inspect
import os
import sys


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
srcdir = os.path.join(parentdir, "givemetheodds")
sys.path.insert(0, srcdir)


import pytest
from pathlib import Path
from mission_service import MissionService


@pytest.fixture
def current_file_path():
    return os.path.dirname(os.path.realpath(__file__))


def test_get_mission_success_odds_from_file(current_file_path):
    mission_details_file_path: str = os.path.join(current_file_path, "sample_inputs/millennium-falcon.json")
    mission_service: MissionService = MissionService(mission_details_file_path=Path(mission_details_file_path))
    intercepted_data_file_path: str = os.path.join(current_file_path, "sample_inputs/empire.json")
    expected = 0

    actual = mission_service.get_mission_success_odds(intercepted_data=Path(intercepted_data_file_path))

    assert actual == expected


def test_get_mission_success_odds_from_dict(current_file_path):
    mission_details_file_path: str = os.path.join(current_file_path, "sample_inputs/millennium-falcon.json")
    mission_service: MissionService = MissionService(mission_details_file_path=Path(mission_details_file_path))
    intercepted_data = {
        "countdown": 6,
        "bounty_hunters": [
            {"planet": "Tatooine", "day": 4},
            {"planet": "Dagobah", "day": 5}
        ]
    }

    expected = 0

    actual = mission_service.get_mission_success_odds(intercepted_data=intercepted_data)

    assert actual == expected
