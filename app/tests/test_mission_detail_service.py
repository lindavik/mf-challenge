import json

import pytest

from app.mission_detail_service import MissionDetails, MissionConverter


def test_get_mission_details():
    details = {
        "autonomy": 6,
        "departure": "Tatooine",
        "arrival": "Endor",
        "routes_db": "universe.db"
    }
    expected = MissionDetails(autonomy=6,
                            departure="Tatooine",
                            arrival="Endor",
                            routes="universe.db")

    actual = MissionConverter.get_mission_details(details)

    assert actual == expected


def test_get_mission_details_bad_field_format():
    details = {
        "autonomy": "6",
        "departure": "Tatooine",
        "arrival": "Endor",
        "routes_db": "universe.db"
    }
    with pytest.raises(Exception):
        MissionConverter.get_mission_details(details)


def test_get_mission_details_with_unknown_fields():
    details = {
        "autonomy": 6,
        "departure": "Tatooine",
        "arrival": "Endor",
        "routes_db": "universe.db",
        "should_not_be_here": "nope"
    }

    expected = MissionDetails(autonomy=6,
                            departure="Tatooine",
                            arrival="Endor",
                            routes="universe.db")

    actual = MissionConverter.get_mission_details(details)

    assert actual == expected


def test_get_mission_details_missing_required_details():
    with pytest.raises(Exception):
        details = {
            "autonomy": 6,
            "arrival": "Endor",
            "routes_db": "universe.db"
        }
        MissionConverter.get_mission_details(details)


def test_get_mission_details_invalid_autonomy():
    with pytest.raises(Exception):
        details = {
            "autonomy": -6,
            "arrival": "Endor",
            "departure": "Tatooine",
            "routes_db": "universe.db"
        }
        MissionConverter.get_mission_details(details)