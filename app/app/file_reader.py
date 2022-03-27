import json
import logging
import pathlib

logging.getLogger().addHandler(logging.StreamHandler())


class FileReader:

    @staticmethod
    def read_json(path_to_file: str):
        file_extension = pathlib.Path(path_to_file).suffix
        if file_extension == ".json":
            try:
                with open(path_to_file) as json_file:
                    return json.load(json_file)
            except Exception:
                logging.exception(f"\nError occurred while loading {path_to_file}.")
                raise InputFileReadError()
        else:
            logging.error(f"Incorrect file extension. Expected .json, got {file_extension}")
            raise InputFileReadError()


class InputFileReadError(Exception):
    """Exception raised when input files are in an incorrect format/corrupt.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="Input files do not match expected format. "
                               "Please see sample input files for more details."):
        self.message = message
        super().__init__(self.message)
