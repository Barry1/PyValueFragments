"""Identifier file for package and building namespace."""

import logging

from .contextmanagers import (
    TimingCM,
    LinuxTimeCM,
    NoOutput,
)
from .decorators import (
    linuxtime,
    logdecorate,
    memoize,
    moduleexport,
    portable_timing,
    timing_process_time,
    timing_thread_time,
    timing_wall,
)
from .helpers import (
    backgroundme,
    basic_auth,
    closeifrunningloky,
    eprint,
    file_exists_current,
    filecache,
    int2bin,
    pi_for_cpu_load,
    recurse_files_in_folder,
)  # pylint: disable=E0401,E0402 # noqa: W0401,W0611
from .mathhelpers import easybisect, intp, polyroot

# <https://docs.python.org/3/howto/logging.html#library-config>
thevaluefragmentslogger: logging.Logger = logging.getLogger(name=__name__)
thevaluefragmentslogger.addHandler(hdlr=logging.NullHandler())
thevaluefragmentslogger.info(msg="valuefragments __init__")
__all__: list[str] = [
    "backgroundme",
    "basic_auth",
    "closeifrunningloky",
    "easybisect",
    "eprint",
    "file_exists_current",
    "filecache",
    "int2bin",
    "intp",
    "linuxtime",
    "LinuxTimeCM",
    "logdecorate",
    "memoize",
    "moduleexport",
    "NoOutput",
    "pi_for_cpu_load",
    "polyroot",
    "portable_timing",
    "recurse_files_in_folder",
    "timing_process_time",
    "timing_thread_time",
    "timing_wall",
    "TimingCM",
]
