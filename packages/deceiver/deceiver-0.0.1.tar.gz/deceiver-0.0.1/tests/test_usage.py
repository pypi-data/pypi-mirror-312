import pytest

import deceiver


def test_basic_usage():
    class APIIllusion(deceiver.Illusion):
        some_attr = None

        def __init__(self) -> None:
            super().__init__()

        def some_method(self, arg: str | None = None):
            return None

    api_illusion = APIIllusion()

    with pytest.raises(AttributeError, match='unknown_attr'):
        api_illusion.unknown_attr

    assert api_illusion.some_attr is None
    assert api_illusion.some_method() is None
    assert api_illusion.some_method("some_argument") is None

    assert api_illusion.__deceiver_log__ == [
        '[call] __init__ (*(), **{}) -> None',
        '[get] some_attr -> None',
        '[call] some_method (*(), **{}) -> None',
        "[call] some_method (*('some_argument',), **{}) -> None",
    ]
