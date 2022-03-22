from app.main import main


def test_main():
    actual = main()
    expected = "result"

    assert actual == expected
