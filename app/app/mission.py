from app.prediction_service import PredictionService


class Mission(object):
    def __init__(self, mission_details, intercepted_data):
        self.mission_details = mission_details
        self.intercepted_data = intercepted_data
        self.prediction_service = PredictionService()

    def get_mission_outcome(self):
        return self.prediction_service.get_probability_of_success()
