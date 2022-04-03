import sys
from pathlib import Path

import typer
from givemetheodds.mission_service import MissionService

app = typer.Typer()


@app.command()
def get_odds(
    mission_details_file_path: Path = typer.Argument(
        ...,
        help="The path to the file containing the Millennium Falcon mission details",
    ),
    intercepted_data_file_path: Path = typer.Argument(
        ..., help="The path to the file containing the rebel intercepted data"
    ),
):
    """
    Gives the odds of the Millennium Falcon reaching the destination planet in time without getting captured by bounty hunters.
    Takes two input files: a file containing the Millennium Falcon mission details and a file containing the rebel intercepted data.
    You can read more about the challenge here: https://github.com/dataiku/millenium-falcon-challenge
    """
    try:
        mission_service = MissionService(
            mission_details_file_path=mission_details_file_path
        )
        odds = mission_service.get_mission_success_odds(
            intercepted_data=intercepted_data_file_path
        )
        typer.echo(odds)
    except:
        typer.echo(
            "An error occurred. Please make sure that the file paths and formats are correct."
        )
        sys.exit(1)


if __name__ == "__main__":
    app()
