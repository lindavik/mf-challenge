from pathlib import Path

from givemetheodds.prediction_service import PredictionService
from givemetheodds.context import ContextLoader


class MissionService:

    def __init__(self, mission_details_file_path: Path):
        mission_details = ContextLoader.load_mission_details(file_path=str(mission_details_file_path))
        self.prediction_service = PredictionService(mission_details=mission_details)

    def get_mission_success_odds(self, intercepted_data):
        """
        Calculates the probability of successfully reaching the destination planet without
        being captured by bounty hunters.
        :param intercepted_data: path to intercepted data file or json representation of the intercepted data
        :return: probability of success. Returns a number ranging from 0 to 100.
        """
        if isinstance(intercepted_data, Path):
            intercepted_data = ContextLoader.load_intercepted_data_from_file(file_path=str(intercepted_data))
            return self.prediction_service.get_probability_of_success(countdown=intercepted_data.countdown,
                                                                      hunter_schedule=intercepted_data.bounty_hunter_schedule)
        else:
            intercepted_data = ContextLoader.load_intercepted_data(raw_intercepted_data=intercepted_data)
            return self.prediction_service.get_probability_of_success(countdown=intercepted_data.countdown,
                                                                      hunter_schedule=intercepted_data.bounty_hunter_schedule)
