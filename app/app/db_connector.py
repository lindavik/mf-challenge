import sqlite3
import logging
from os.path import exists
from sqlite3 import Connection, Cursor
from typing import Iterator

logging.getLogger().addHandler(logging.StreamHandler())


class DBConnector:

    @staticmethod
    def _create_connection(db_file: str):
        """Creates a database connection to the SQLite database
            specified by db_file
        :param db_file: database file
        :return: Connection object or raises Exception
        """
        file_exists = exists(db_file)
        if file_exists:
            try:
                conn: Connection = sqlite3.connect(db_file)
                logging.debug(f"Successfully connected to DB: {db_file}")
                return conn
            except:
                logging.exception(f"Could not connect to DB: {db_file}")
                raise DatabaseConnectionException()
        else:
            raise DatabaseFileNotFound()

    @staticmethod
    def get_iterator(db_file: str, query: str) -> Iterator:
        """
        Creates an iterator for iterating over the results of a database query.
        :param db_file: database file provided
        :param query: query to be run against database
        :return: iterator for iterating over results
        """
        connection = DBConnector._create_connection(db_file=db_file)
        if connection is not None:
            iterator: Cursor = connection.cursor()
            return iterator.execute(query)


class DatabaseFileNotFound(Exception):
    """
    Exception raised when the required file is not found.
    """

    def __init__(self, message="Database file not found."):
        self.message = message
        super().__init__(self.message)


class DatabaseConnectionException(Exception):
    """
    Exception raised when connecting to the database.
    """

    def __init__(self, message="Could not connect to database."):
        self.message = message
        super().__init__(self.message)