# import inspect
# import os
# import sys
#
# currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
# parentdir = os.path.dirname(currentdir)
# sys.path.insert(0, parentdir)
#
# import click
# import pytest
# import click.testing
#
# from backend import cli
# from pathlib import Path
#
#
# @pytest.fixture
# def runner() -> click.testing.CliRunner:
#     """Fixture for invoking command-line interfaces."""
#     return click.testing.CliRunner()
#
#
# def test_get_odds(runner: click.testing.CliRunner) -> None:
#     """It uses the specified filepath."""
#     result = runner.invoke(cli.hello_world)
#     assert result.exit_code == 0
#
#     result = runner.invoke(cli.get_odds, [Path('default_inputs/millennium-falcon.json'),
#                                           Path('default_inputs/empire.json')])
#     assert result.exit_code == 0