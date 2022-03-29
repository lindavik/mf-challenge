from sqlite3 import Connection

import pytest

from app.db_connector import DBConnector, DatabaseFileNotFound


def test_create_connection():
    db_file: str = './sample_inputs/universe.db'
    actual: Connection = DBConnector._create_connection(db_file)

    assert actual is not None


def test_create_connection_no_db_file():
    with pytest.raises(DatabaseFileNotFound):
        db_file: str = './sample_inputs/universe23.db'
        DBConnector._create_connection(db_file)


def test_get_iterator():
    db_file: str = './sample_inputs/universe.db'
    query: str = "SELECT origin, destination, travel_time FROM routes"
    actual = DBConnector.get_iterator(db_file=db_file, query=query)

    assert actual is not None
