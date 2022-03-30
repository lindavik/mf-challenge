import inspect
import os
import sys

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from typer.testing import CliRunner

from cli import app

runner = CliRunner()


def test_get_odds():
    expected_exit_code = 0
    expected_odds = "0"

    result = runner.invoke(app, ["tests/sample_inputs/millennium-falcon.json", "tests/sample_inputs/empire.json"])

    assert result.exit_code == expected_exit_code
    assert expected_odds in result.stdout


def test_get_odds_missing_both_args():
    expected_exit_code = 2

    result = runner.invoke(app, [])

    assert result.exit_code == expected_exit_code


def test_get_odds_missing_one_arg():
    expected_exit_code = 2

    result = runner.invoke(app, ["./sample_inputs/millennium-falcon.json"])

    assert result.exit_code == expected_exit_code


def test_get_odds_broken_path():
    expected_exit_code = 1

    result = runner.invoke(app, ["./sample_inputs/millennium-falcon.json", "./sample_inputs/nope.json"])

    assert result.exit_code == expected_exit_code
