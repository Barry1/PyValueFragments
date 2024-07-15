"""Identifier file for package and building namespace."""

import logging

from .contextmanagers import *  # pylint: disable=E0401,E0402 # noqa: W0401,W0611
from .decorators import *  # pylint: disable=E0401,E0402 # noqa: W0401,W0611
from .helpers import *  # pylint: disable=E0401,E0402 # noqa: W0401,W0611

__all__: list[str] = []
from .mathhelpers import easybisect, intp, polyroot

# <https://docs.python.org/3/howto/logging.html#library-config>


thevaluefragmentslogger: logging.Logger = logging.getLogger(__name__)
thevaluefragmentslogger.addHandler(logging.NullHandler())
thevaluefragmentslogger.info("valuefragments __init__")


# __all__.append(
#        "backgroundme",
#        "basic_auth",
#        "easybisect",
#        "eprint",
#        "hashfile",
#        "ic",
#        "intp",
#        "linuxtime",
#        "LinuxTimeCM",
#        "loadallcores",
#        "loadonecore",
#        "memoize",
#        "NoOutput",
#        "polyroot",
#        "portable_timing",
#        "recurse_files_in_folder",
#        "run_grouped_in_ppe",
#        "run_grouped_in_tpe",
#        "stringtovalidfilename",
#        "timing_process_time",
#        "timing_psutil",
#        "timing_resource",
#        "timing_thread_time",
#        "timing_wall",
#        "TimingCM",
#        "to_inner_task",
# )
