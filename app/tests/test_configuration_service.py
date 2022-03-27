import json

import pytest

from app.file_reader import MissionDetails, parse_falcon_input, MissingMissionDetailsError


def test_parse_falcon_input():
    path_to_file: str = "sample_inputs/millenium_falcon/millennium-falcon.json"
    expected = MissionDetails(autonomy=6, departure="Tatooine", arrival="Endor")

    actual: MissionDetails = parse_falcon_input(path_to_file)

    assert actual == expected


def test_parse_falcon_input_missing_fields():
    with pytest.raises(MissingMissionDetailsError):
        path_to_file: str = "sample_inputs/millenium_falcon/millennium-falcon-incomplete.json"
        parse_falcon_input(path_to_file)
