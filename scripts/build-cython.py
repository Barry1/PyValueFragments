"""Build module for Cython compilation.
More details could be read and found under
<https://python-poetry.org/docs/building-extension-modules/#cython>
Happy Reading!
"""

from Cython.Build import cythonize
from setuptools import setup


def build() -> None:
    """Dummy Build function to run Cython."""
    print("Ab geht es.")
    setup(
        name="valuefragments",
        ext_modules=cythonize("src/valuefragments/mathhelpers.py", show_all_warnings=True),
    )
    print("feddich")


if __name__ == "__main__":
    build()
