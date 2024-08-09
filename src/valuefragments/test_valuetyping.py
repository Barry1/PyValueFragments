from sys import version_info

import valuefragments.valuetyping

if version_info[:2] == (3, 11):

    def test_pythreeeleven() -> None:
        from valuefragments.valuetyping import LiteralString, TypeIs

        assert TypeIs.__module__ == "typing_extensions"
        assert LiteralString.__module__ == "typing"


if version_info[:2] == (3, 12):

    def test_pythreetwelve() -> None:
        from valuefragments.valuetyping import TypeAliasType, TypeIs

        assert TypeIs.__module__ == "typing_extensions"
        assert TypeAliasType.__module__ == "typing"
