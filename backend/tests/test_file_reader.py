import os

import pytest

from backend.file_reader import FileReader, InputFileReadError


@pytest.fixture
def test_file_path():
    return os.path.dirname(os.path.realpath(__file__))


def test_read_json(test_file_path):
    mission_details_file_path: str = os.path.join(test_file_path, "sample_inputs/millenium_falcon/millennium-falcon.json")

    expected = {
        "autonomy": 6,
        "departure": "Tatooine",
        "arrival": "Endor",
        "routes_db": "universe.db"
    }

    actual = FileReader.read_json(mission_details_file_path)

    assert actual == expected


def test_read_json_corrupt_file(test_file_path):
    file_path: str = os.path.join(test_file_path, "sample_inputs/millenium_falcon/millennium-falcon-corrupt.json")

    with pytest.raises(InputFileReadError):
        FileReader.read_json(file_path)


def test_read_json_wrong_extension(test_file_path):
    file_path: str = os.path.join(test_file_path, "sample_inputs/millenium_falcon/millennium-falcon.txt")

    with pytest.raises(InputFileReadError):
        FileReader.read_json(file_path)


def test_read_json_missing_file(test_file_path):
    file_path: str = os.path.join(test_file_path, "sample_inputs/millenium_falcon/s.json")

    with pytest.raises(InputFileReadError):
        FileReader.read_json(file_path)
