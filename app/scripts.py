import os


def test():
    os.system("pytest")


def reformat():
    os.system("shed --refactor")


def coverage():
    os.system("pytest --cov=app tests")
