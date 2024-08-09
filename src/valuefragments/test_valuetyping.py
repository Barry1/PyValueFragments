"""Version specific tests if import mechanism is working."""

from sys import version_info

if version_info[:2] == (3, 11):
    # <https://docs.python.org/3/whatsnew/3.11.html#typing>

    def test_pythreeeleven() -> None:
        """In 3.11 LiteralString was introduced but TypIs not yet."""
        from valuefragments.valuetyping import (
            LiteralString,
            TypeIs,
            assert_never,
            assert_type,
            reveal_type,
        )

        assert TypeIs.__module__ == "typing_extensions"
        assert LiteralString.__module__ == "typing"
        assert assert_never.__module__ == "typing"
        assert assert_type.__module__ == "typing"
        assert reveal_type.__module__ == "typing"


if version_info[:2] == (3, 12):
    # <https://docs.python.org/3/whatsnew/3.12.html#typing>

    def test_pythreetwelve() -> None:
        """In 3.12 TypeAliasType was introduced but TypIs not yet."""
        from valuefragments.valuetyping import TypeAliasType, TypeIs, override

        assert TypeIs.__module__ == "typing_extensions"
        assert TypeAliasType.__module__ == "typing"
        assert override.__module__ == "typing"
