import pytest

from app.intercepted_converter import InterceptedData, InterceptedDataConverter
from tests.shared_test_utils import HOTH, ENDOR


def test_map_to_intercepted_data():
    bounty_hunter_schedule = {
        HOTH: {6, 7, 8},
        ENDOR: {9}
    }
    raw_data = {
        "countdown": 7,
        "bounty_hunters": [
            {"planet": "Hoth", "day": 6},
            {"planet": "Hoth", "day": 7},
            {"planet": "Hoth", "day": 8},
            {"planet": "Endor", "day": 9}
        ]
    }
    expected = InterceptedData(countdown=7, bounty_hunter_schedule=bounty_hunter_schedule)

    actual = InterceptedDataConverter.map_to_intercepted_data(raw_data=raw_data)

    assert actual == expected


def test_process_schedule():
    raw_schedule = [
        {"planet": "Hoth", "day": 6},
        {"planet": "Hoth", "day": 7},
        {"planet": "Hoth", "day": 8},
        {"planet": "Endor", "day": 9}
    ]
    expected = {
        HOTH: {6, 7, 8},
        ENDOR: {9}
    }

    actual = InterceptedDataConverter._process_schedule(raw_schedule=raw_schedule)

    assert actual == expected
