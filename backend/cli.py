from pathlib import Path

import typer

from mission_service import MissionService


def get_odds(
        mission_details_file_path: Path = typer.Argument(...,
                                                           help="The path to the file containing the Millennium Falcon mission details"),
        intercepted_data_file_path: Path = typer.Argument(...,
                                                help="The path to the file containing the rebel intercepted data")):
    """
    Gives the odds of the Millennium Falcon reaching the destination planet in time without getting captured by bounty hunters.
    Takes two input files: a file containing the Millennium Falcon mission details and a file containing the rebel intercepted data.
    """
    mission_service = MissionService(mission_details_file_path=mission_details_file_path)
    odds = mission_service.get_mission_success_odds(intercepted_data=intercepted_data_file_path)
    typer.echo(odds)


if __name__ == "__main__":
    typer.run(get_odds)
