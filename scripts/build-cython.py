"""Build module for Cython compilation.
More details could be read and found under
<https://python-poetry.org/docs/building-extension-modules/#cython>
Happy Reading!
"""

from Cython.Build import cythonize
from setuptools import setup

# print(__import__("sys").version)


def build() -> None:
    """Dummy Build function to run Cython."""
    print("Before setup.")
    setup(
        name="valuefragments",
        ext_modules=cythonize("src/valuefragments/mathhelpers.py"),  # , show_all_warnings=True),
    )
    print("After setup.")


if __name__ == "__main__":
    build()
