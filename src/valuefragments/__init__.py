"""Identifier file for package and building namespace."""

import logging

from .contextmanagers import LinuxTimeCM, NoOutput, TimingCM
from .decorators import (
    linuxtime,
    logdecorate,
    memoize,
    portable_timing,
    timing_process_time,
    timing_thread_time,
    timing_wall,
)
from .helpers import (  # pylint: disable=E0401,E0402 # noqa: W0401,W0611; backgroundme,
    basic_auth,
    closeifrunningloky,
    eprint,
    file_exists_current,
    filecache,
    getselectedhreflinks,
    hashfile,
    int2bin,
    pi_for_cpu_load,
    recurse_files_in_folder,
    run_grouped,
    thread_native_id_filter,
)
from .mathhelpers import easybisect, intp, polyroot, probneeds
from .moduletools import moduleexport

# <https://docs.python.org/3/howto/logging.html#library-config>
thevaluefragmentslogger: logging.Logger = logging.getLogger(name=__name__)
thevaluefragmentslogger.addHandler(hdlr=logging.NullHandler())
thevaluefragmentslogger.info(msg="valuefragments __init__")
__all__: list[str] = [
    #    "backgroundme",
    "basic_auth",
    "closeifrunningloky",
    "easybisect",
    "eprint",
    "file_exists_current",
    "filecache",
    "getselectedhreflinks",
    "hashfile",
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
    "probneeds",
    "recurse_files_in_folder",
    "run_grouped",
    "timing_process_time",
    "timing_thread_time",
    "timing_wall",
    "TimingCM",
    "thread_native_id_filter",
]
