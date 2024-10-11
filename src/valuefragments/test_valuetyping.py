#!/usr/bin/env -S pytest
"""Version specific tests if import mechanism is working."""

from sys import version_info

"""Should run in any environment after
python -m pip install --upgrade typing_extensions pytest pip pytest-asyncio
pytest
"""


# Should run in any environment after
# python -m pip install --upgrade typing_extensions pytest pip pytest-asyncio
# pytest
if version_info[:2] == (3, 11):
    # <https://docs.python.org/3/whatsnew/3.11.html#typing>

    def test_pythreeeleven() -> None:
        """In 3.11 LiteralString was introduced but TypeIs not yet."""
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
        """In 3.12 TypeAliasType was introduced but TypeIs not yet."""
        from valuefragments.valuetyping import TypeAliasType, TypeIs, override

        assert TypeIs.__module__ == "typing_extensions"
        assert TypeAliasType.__module__ == "typing"
        assert override.__module__ == "typing"


if version_info[:2] == (3, 13):
    # <https://docs.python.org/3/whatsnew/3.12.html#typing>

    def test_pythreethirteen() -> None:
        """In 3.13 ."""
        """
        import typing
        import typing_extensions
        t1=set(dir(typing))
        t2=set(dir(typing_extensions))
        t2.difference(t1)
        """
        from valuefragments.valuetyping import CapsuleType, TypeIs

        assert CapsuleType.__module__ == "builtins"
        assert TypeIs.__module__ == "typing"
