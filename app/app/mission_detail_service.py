   def parse_falcon_input(path_to_file: str) -> MissionDetails:
        with open(path_to_file) as json_file:
            data = json.load(json_file)

        try:
            details = MissionDetails(autonomy=data["autonomy"],
                                     departure=data["departure"],
                                     arrival=data["arrival"])
            return details
        except KeyError:
            raise MissingMissionDetailsError()

class MissionDetails(object):
    def __init__(self, autonomy: int, departure: str, arrival: str):
        self.autonomy = autonomy
        self.departure = departure
        self.arrival = arrival
        # self.routes = dict()

    @property
    def autonomy(self):
        return self._autonomy

    @autonomy.setter
    def autonomy(self, autonomy):
        if not (autonomy > 0): raise Exception("autonomy must be a greater than 0")
        self._autonomy = autonomy

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, MissionDetails):
            return (self.autonomy == other.autonomy and
                    self.departure == other.departure and
                    self.arrival == other.arrival)

        return False


class MissingMissionDetailsError(Exception):
    """Exception raised when Millennium Falcon mission input file is missing required details.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message="Missing details in mission detail input file. "
                               "Required fields are: autonomy, departure, arrival and route_db"):
        self.message = message
        super().__init__(self.message)


def parse_falcon_input(path_to_file: str) -> MissionDetails:
    with open(path_to_file) as json_file:
        data = json.load(json_file)

    try:
        details = MissionDetails(autonomy=data["autonomy"],
                                 departure=data["departure"],
                                 arrival=data["arrival"])
        return details
    except KeyError:
        raise MissingMissionDetailsError()