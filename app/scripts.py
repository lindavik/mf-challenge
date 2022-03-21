import os


def test():
    os.system("pytest")


def reformat():
    os.system("shed --refactor")
