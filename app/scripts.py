import os


def test():
    os.system("python -m pytest")


def reformat():
    os.system("shed --refactor")


def coverage():
    os.system("pytest --cov=app --cov-fail-under=95 tests")
