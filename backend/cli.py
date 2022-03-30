from pathlib import Path

import typer


def get_odds(
        millennium_falcon_file_path: Path = typer.Argument(...,
                                                           help="The path to the file containing the Millennium Falcon mission details"),
        empire_file_path: Path = typer.Argument(...,
                                                help="The path to the file containing the rebel intercepted data")):
    """
    Gives the odds of the Millennium Falcon reaching the destination planet in time without getting captured by bounty hunters.
    Takes two input files: a file containing the Millennium Falcon mission details and a file containing the rebel intercepted data.
    """
    typer.echo(f"Hello {millennium_falcon_file_path}, {empire_file_path}")


if __name__ == "__main__":
    typer.run(get_odds)
