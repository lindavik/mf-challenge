import os
from sqlite3 import Connection

import pytest

from givemetheodds.db_connector import DBConnector, DatabaseFileNotFound


@pytest.fixture
def current_file_path():
    return os.path.dirname(os.path.realpath(__file__))


def test_create_connection(current_file_path):
    db_file: str = os.path.join(current_file_path, "sample_inputs/universe.db")
    actual: Connection = DBConnector._create_connection(db_file)

    assert actual is not None


def test_create_connection_no_db_file(current_file_path):
    with pytest.raises(DatabaseFileNotFound):
        db_file: str = os.path.join(current_file_path, "sample_inputs/universe23.db")
        DBConnector._create_connection(db_file)


def test_get_iterator(current_file_path):
    db_file: str = os.path.join(current_file_path, "sample_inputs/universe.db")
    query: str = "SELECT origin, destination, travel_time FROM routes"
    actual = DBConnector.get_iterator(db_file=db_file, query=query)

    assert actual is not None

