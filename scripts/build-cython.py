"""Build module for Cython compilation.
More details could be read and found under
<https://python-poetry.org/docs/building-extension-modules/#cython>
Happy Reading!
"""

from Cython.Build import cythonize

# ModuleNotFoundError
from setuptools import setup

# print(__import__("sys").version)


def build() -> None:
    """Dummy Build function to run Cython."""
    setup(
        name="valuefragments",
        # , show_all_warnings=True),
        ext_modules=cythonize(
            module_list="src/valuefragments/mathhelpers.py",
            exclude_failures=True,
            show_all_warnings=True,
        ),
        # https://cython.readthedocs.io/en/latest/src/userguide/source_files_and_compilation.html#Cython.Build.cythonize
        script_args=["build_ext", "--inplace"],
    )


if __name__ == "__main__":
    build()
