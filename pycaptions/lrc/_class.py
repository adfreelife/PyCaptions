from ..development import CaptionsFormat

from .functions import detectLRC, readLRC, saveLRC

class LyRiCs(CaptionsFormat):
    """
    Synchronized Accessible Media Interchange

    Read more about it https://learn.microsoft.com/en-us/previous-versions/windows/desktop/dnacc/understanding-sami-1.0

    Example:

    with SAMI("path/to/file.sami") as sami:
        sami.saveSRT("file")
    """
    detect = staticmethod(detectLRC)
    read = readLRC
    save = saveLRC

    from ..development.readers import (
        # readSAMI, readUSF,
        readSRT, readSUB,
        readTTML, readVTT
    )
