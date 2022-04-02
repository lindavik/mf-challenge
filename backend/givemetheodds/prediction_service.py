import logging
from typing import Dict, List, Tuple

from givemetheodds.converters import MissionDetails, PlanetGraph

logging.getLogger().addHandler(logging.StreamHandler())


class PredictionService:
    def __init__(self, mission_details: MissionDetails):
        self.autonomy: int = mission_details.autonomy
        self.departure: str = mission_details.departure
        self.destination: str = mission_details.arrival
        self.planet_graph: PlanetGraph = mission_details.routes
        self.paths = []

    def get_probability_of_success(self, countdown: int, hunter_schedule: Dict) -> int:
        """
        Calculates the probability of successfully reaching the destination planet without
        being captured by bounty hunters. Returns a number ranging from 0 to 100.
        :param countdown: positive integer indicating the number of days before the Death Star annihilates Endor
        :param hunter_schedule: list of all locations where Bounty Hunter are scheduled to be present
        :return: a non-negative integer (0-100) indicating the probability (%) of successfully reaching the destination planet
        without being captured by bounty hunters
        """
        self._generate_all_paths_between_two_planets(
            time_limit=countdown,
            destination_planet=self.destination,
            start_planet=self.departure,
        )
        if not self.paths:
            logging.info("No paths were found")
            return 0

        detailed_travel_plans = [
            self._get_detailed_travel_plan(plan) for plan in self.paths
        ]
        optimized_paths = [
            self._optimize_path(plan, hunter_schedule, countdown=countdown)
            for plan in detailed_travel_plans
        ]

        capture_attempt_count: int = PredictionService._get_lowest_capture_count(
            hunter_schedule=hunter_schedule, optimized_paths=optimized_paths
        )
        probability_of_capture: float = PredictionService._get_probability_of_capture(
            capture_attempt_count=capture_attempt_count
        )
        return PredictionService._convert_capture_probability_to_success_rate(
            probability_of_capture=probability_of_capture
        )

    def _generate_all_paths_between_two_planets(self, start_planet: str, destination_planet: str,
                                                time_limit: int) -> None:
        """
        Generates a list of all paths between two planets.
        :param start_planet: the start planet
        :param destination_planet: the destination planet
        :param time_limit: the time limit in days to reach the destination planet
        :return: None
        """
        visited = {planet: False for planet in self.planet_graph.planets}
        path = []
        self._generate_all_paths(start_planet, destination_planet, visited, path, time_limit)

    def _generate_all_paths(self, current_planet: str, destination_planet: str, visited: Dict, path: List,
                            time_limit: int) -> None:
        """
        Generates a list of all paths between the planets.
        :param current_planet: the current planet
        :param destination_planet: the destination planet
        :param visited: a dictionary with the planet as the key and boolean of if it was visited
        :param path: the path
        :param time_limit: the time limit
        :return: None
        """
        visited[current_planet] = True
        path.append(current_planet)

        travel_time: int = self._get_travel_in_days(path)
        if travel_time > time_limit:
            logging.info(f"{path} exceeded the time limit.")
        elif current_planet == destination_planet:
            logging.info(f"Found path: {path}")
            self.paths.append(path.copy())
        else:
            for neighbour_node in self.planet_graph.routes[current_planet]:
                if not visited[neighbour_node]:
                    self._generate_all_paths(
                        neighbour_node, destination_planet, visited, path, time_limit
                    )
        path.pop()
        visited[current_planet] = False

    def _get_detailed_travel_plan(self, path: List) -> List:
        travel_plan = []
        total = 0
        current_fuel: int = self.autonomy
        refuelling_day: int = 1

        if not path:
            return travel_plan

        for i in range(0, len(path) - 1):
            travel_plan.append((path[i], total))

            next_hop_in_days = self.planet_graph.distances[(path[i], path[i + 1])]

            if current_fuel < next_hop_in_days:
                total += refuelling_day
                current_fuel += self.autonomy
                travel_plan.append((path[i], total))

            total += next_hop_in_days
            current_fuel -= next_hop_in_days
        travel_plan.append((path[-1], total))
        return travel_plan

    def _get_travel_in_days(self, path: List):
        total = 0
        current_fuel: int = self.autonomy
        refuelling_day: int = 1
        for i in range(0, len(path) - 1):
            next_hop_in_days = self.planet_graph.distances[(path[i], path[i + 1])]
            if current_fuel < next_hop_in_days:
                total += next_hop_in_days + refuelling_day
                current_fuel += self.autonomy - next_hop_in_days
            else:
                total += next_hop_in_days
                current_fuel -= next_hop_in_days

        return total

    @staticmethod
    def _get_lowest_capture_count(hunter_schedule, optimized_paths):
        best_current = None
        for path in optimized_paths:
            capture_attempt_count = PredictionService._get_capture_attempt_count(
                route=path, hunter_schedule=hunter_schedule
            )
            if best_current == 0:
                break
            if best_current is None or capture_attempt_count < best_current:
                best_current = capture_attempt_count
        return best_current

    @staticmethod
    def _adjust_for_fuelling_needs(route: List, autonomy: int) -> List:
        new_route: List = []
        deviation: int = 0
        last_item = route[-1]
        fuel_budget: int = autonomy

        for i in range(len(route)):
            current_leg = route[i]
            new_route.append((current_leg[0], current_leg[1] + deviation))
            if current_leg != last_item:
                next_leg = route[i + 1]
                next_flight_distance = next_leg[1] - current_leg[1]
                if next_flight_distance > fuel_budget:
                    deviation += 1
                    fuel_budget = autonomy
                    new_route.append((current_leg[0], current_leg[1] + deviation))
                fuel_budget = fuel_budget - next_flight_distance

        return new_route

    @staticmethod
    def _get_capture_attempt_count(route: List, hunter_schedule: List):
        """
        Gets the number of capture attempts/overlapping stops between the shortest list and the hunter schedule.
        :param route: path from departure planet to destination planet
        :param hunter_schedule: bounty hunter schedule
        :return: number of capture attempts by bounty hunters
        """
        capture_attempts: int = 0
        for stop in route:
            if stop in hunter_schedule:
                capture_attempts += 1
        return capture_attempts

    @staticmethod
    def _convert_capture_probability_to_success_rate(
            probability_of_capture: float,
    ) -> int:
        """
        Converts the probability of capture to the success rate.
        :param probability_of_capture: the probability of capture (ranging from 0.0 to 1.0)
        :return: the success rate (ranging from 0 - 100)
        """
        probability_of_success: float = 1 - probability_of_capture
        return int(round(probability_of_success, 2) * 100)

    @staticmethod
    def _get_probability_of_capture(capture_attempt_count: int) -> float:
        """
        Calculates the probability of getting captured depending on the number of capture attempts.
        :param capture_attempt_count: number of capture attempts
        :return: the probability of getting captured
        """
        result: float = 0.0

        if capture_attempt_count == 0:
            return result

        for i in range(capture_attempt_count):
            result += (9 ** (i)) / (10 ** (i + 1))

        return result

    @staticmethod
    def _can_avoid_bounty_hunters_set(stop: Tuple, delay_budget: int, hunter_schedule):
        for day in range(delay_budget + 1):
            if (stop[0], stop[1] + day) not in hunter_schedule:
                return True
        return False

    @staticmethod
    def _optimize_path(path, hunter_schedule, countdown):
        arrival_day: int = path[-1][1]
        delay_budget: int = countdown - arrival_day
        waiting_day = 1
        new_path: List = []
        delay = 0
        previous_stop = None

        if delay_budget == 0:
            return path

        for stop in path:
            if previous_stop is not None and stop[0] == previous_stop[0]:
                new_path.append((stop[0], stop[1] + delay))
            elif (
                    new_path
                    and stop in hunter_schedule
                    and PredictionService._can_avoid_bounty_hunters_set(
                stop, delay_budget, hunter_schedule
            )
                    and delay_budget != 0
            ):
                last_stop = new_path[-1]
                new_stop = (last_stop[0], last_stop[1] + waiting_day)
                new_path.append(new_stop)
                delay_budget -= waiting_day
                delay += waiting_day
                stop = (stop[0], stop[1] + delay)

                while stop in hunter_schedule and delay_budget != 0:
                    last_stop = new_path[-1]
                    new_stop = (last_stop[0], last_stop[1] + waiting_day)
                    new_path.append(new_stop)
                    delay_budget -= waiting_day
                    delay += waiting_day

                new_path.append((stop[0], stop[1]))

            else:
                new_path.append((stop[0], stop[1] + delay))
            previous_stop = stop
        return new_path
