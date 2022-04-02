import os
from typing import Dict

from givemetheodds.file_reader import FileReader
from givemetheodds.converters import MissionConverter, MissionDetails, InterceptedData, InterceptedDataConverter


class ContextLoader:

    @staticmethod
    def load_mission_details(file_path: str) -> MissionDetails:
        """
        Loads processed and validated mission details from an input file.
        :param file_path: path to the input file containing the mission details
        :return: mission details
        """
        mission_details_raw = FileReader.read_json(file_path)
        directory: str = os.path.dirname(file_path)
        return MissionConverter.map_to_mission_details(mission_details_raw, directory)

    @staticmethod
    def load_intercepted_data_from_file(file_path: str) -> InterceptedData:
        """
        Loads processed and validated intercepted data from an input file.
        :param file_path: path to the input file containing the intercepted data
        :return: intercepted data
        """
        raw_intercepted_data = FileReader.read_json(file_path)
        return InterceptedDataConverter.map_to_intercepted_data(raw_data=raw_intercepted_data)

    @staticmethod
    def load_intercepted_data(raw_intercepted_data: Dict) -> InterceptedData:
        """
        Loads intercepted data from json compatible data.
        :param raw_intercepted_data: json compatible intercepted data
        :return: intercepted data
        """
        return InterceptedDataConverter.map_to_intercepted_data(raw_data=raw_intercepted_data)
