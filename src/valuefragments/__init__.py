"""Identifier file for package and building namespace."""

import logging

from .contextmanagers import *  # pylint: disable=E0401,E0402 # noqa: W0401,W0611
from .decorators import *  # pylint: disable=E0401,E0402 # noqa: W0401,W0611
from .helpers import (
    int2bin,
    file_exists_current,
    eprint,
    basic_auth,
    backgroundme,
)  # pylint: disable=E0401,E0402 # noqa: W0401,W0611
from .mathhelpers import easybisect, intp, polyroot

# <https://docs.python.org/3/howto/logging.html#library-config>
thevaluefragmentslogger: logging.Logger = logging.getLogger(name=__name__)
thevaluefragmentslogger.addHandler(hdlr=logging.NullHandler())
thevaluefragmentslogger.info(msg="valuefragments __init__")
__all__: list[str] = [
    "backgroundme",
    "basic_auth",
    "easybisect",
    "eprint",
    "file_exists_current",
    "ic",
    "int2bin",
    "intp",
    "memoize",
    "polyroot",
    "portable_timing",
    "TimingCM",
]

# __all__.append(
#        "backgroundme",
#        "basic_auth",
#        "eprint",
#        "hashfile",
#        "linuxtime",
#        "LinuxTimeCM",
#        "loadallcores",
#        "loadonecore",
#        "NoOutput",
#        "recurse_files_in_folder",
#        "run_grouped_in_ppe",
#        "run_grouped_in_tpe",
#        "stringtovalidfilename",
#        "timing_process_time",
#        "timing_psutil",
#        "timing_resource",
#        "timing_thread_time",
#        "timing_wall",
#        ,
#        "to_inner_task",
# )
