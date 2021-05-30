"""helper functions and code snippets which are not decorators."""


def ic(*a):  # pylint: disable=invalid-name
    """Just in case package icecream is not available: For logging purposes."""
    if not a:
        return None
    return a[0] if len(a) == 1 else a


if __debug__:
    try:
        from icecream import ic  # type: ignore[import,no-redef] # noqa: F811,W0404
    except ImportError:
        pass  # Fallback to default
    else:
        ic.configureOutput(includeContext=True)  # type: ignore[attr-defined]
try:
    import psutil
except ImportError:
    ic("psutil is not available")
else:

    def backgroundme() -> None:
        """Give this process background priority."""
        if psutil.WINDOWS:
            try:
                # Details <https://archive.is/peWej#PROCESS_MODE_BACKGROUND_BEGIN>
                psutil.Process().nice(0x00100000)  # PROCESS_MODE_BACKGROUND_BEGIN
            except OSError as theerr:
                if theerr.winerror == 402:  # type: ignore # pylint: disable=no-member
                    ic("Prozess was already in background mode.")
                else:
                    print(theerr)
        else:
            psutil.Process().nice(19)


try:
    import hashlib
except ImportError:
    ic("hashlib is not available")
else:

    def hashfile(filename: str, chunklen: int = 128 * 2 ** 12) -> str:
        """Return md5 hash for file."""
        with open(filename, "rb") as thefile:
            file_hash = hashlib.md5()
            chunk = thefile.read(chunklen)
            while chunk:
                file_hash.update(chunk)
                chunk = thefile.read(chunklen)
        return file_hash.hexdigest()


try:
    import cpu_load_generator  # type: ignore[import]
except ImportError:
    pass
else:

    def loadonecore(
        loadduration: int = 10, loadedcore: int = 0, theload: float = 0.5
    ) -> None:
        """Just a helper function to generate load on one given core."""
        cpu_load_generator.load_single_core(
            core_num=loadedcore,
            duration_s=loadduration,
            target_load=theload,
        )

    def loadallcores(loadduration: int = 10, theload: float = 0.5) -> None:
        """Just a helper function to generate load on all cores."""
        cpu_load_generator.load_all_cores(duration_s=loadduration, target_load=theload)
