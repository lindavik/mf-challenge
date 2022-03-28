from app.prediction_service import PredictionService


class Mission(object):
    def __init__(self, mission_details):
        self.mission_details = mission_details



    def get_mission_outcome(self, intercepted_data):
        pass
        # return self.prediction_service.get_probability_of_success(intercepted_data)
