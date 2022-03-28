import logging

from app.context import ContextLoader
from app.mission import Mission

logging.getLogger().addHandler(logging.StreamHandler())


def main():
    mission_details_file: str = "" #todo populate with args
    mission_details = ContextLoader.load_mission_details(file_path=mission_details_file)
    intercepted_data_file: str = "" #todo populate with args
    intercepted_data = ContextLoader.load_intercepted_data(file_path=intercepted_data_file)
    mission = Mission(mission_details=mission_details, intercepted_data=intercepted_data)
    outcome = mission.get_mission_outcome()


if __name__ == '__main__':
    main()
