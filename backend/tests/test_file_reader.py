import pytest

from backend.src.file_reader import FileReader, InputFileReadError


def test_read_json():
    path: str = "sample_inputs/millenium_falcon/millennium-falcon.json"

    expected = {
        "autonomy": 6,
        "departure": "Tatooine",
        "arrival": "Endor",
        "routes_db": "universe.db"
    }

    actual = FileReader.read_json(path)

    assert actual == expected


def test_read_json_corrupt_file():
    path: str = "sample_inputs/millenium_falcon/millennium-falcon-corrupt.json"
    with pytest.raises(InputFileReadError):
        FileReader.read_json(path)


def test_read_json_wrong_extension():
    path: str = "sample_inputs/millenium_falcon/millennium-falcon.txt"
    with pytest.raises(InputFileReadError):
        FileReader.read_json(path)


def test_read_json_missing_file():
    path: str = "sample_inputs/millenium_falcon/s.json"
    with pytest.raises(InputFileReadError):
        FileReader.read_json(path)