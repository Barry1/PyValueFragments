"""helper functions and code snippets which are not decorators"""
if __debug__:
    try:
        from icecream import ic  # type: ignore[import,no-redef] # noqa: F811,W0404
    except ImportError:
        pass  # Fallback to default
    else:
        ic.configureOutput(includeContext=True)  # type: ignore[attr-defined]
try:
    import hashlib
except ImportError:
    ic("hashlib is not available")
else:

    def hashfile(filename: str, chunklen: int = 128 * 2 ** 12) -> str:
        """returning md5 hash for file"""
        with open(filename, "rb") as thefile:
            file_hash = hashlib.md5()
            chunk = thefile.read(chunklen)
            while chunk:
                file_hash.update(chunk)
                chunk = thefile.read(chunklen)
        return file_hash.hexdigest()
