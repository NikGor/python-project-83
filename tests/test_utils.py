from page_analyzer.utils import is_valid


def test_is_valid():
    assert is_valid("https://www.google.com")
    assert not is_valid("not_a_url")
    assert not is_valid("www.google.com")
    assert not is_valid("https://")
    assert not is_valid("")
    assert not is_valid(None)
    assert not is_valid("https://www.google.com/" * 100)
