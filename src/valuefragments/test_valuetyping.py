"""Version specific tests if import mechanism is working."""

from sys import version_info

if version_info[:2] == (3, 11):

    def test_pythreeeleven() -> None:
        """In 3.11 LiteralString was introduced but TypIs not yet."""
        from valuefragments.valuetyping import LiteralString, TypeIs

        assert TypeIs.__module__ == "typing_extensions"
        assert LiteralString.__module__ == "typing"


if version_info[:2] == (3, 12):

    def test_pythreetwelve() -> None:
        """In 3.12 TypeAliasType was introduced but TypIs not yet."""
        from valuefragments.valuetyping import TypeAliasType, TypeIs

        assert TypeIs.__module__ == "typing_extensions"
        assert TypeAliasType.__module__ == "typing"
