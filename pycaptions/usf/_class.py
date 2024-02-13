from ..development import CaptionsFormat

from .functions import detectUSF, readUSF, saveUSF


class USF(CaptionsFormat):
    """
    Universal Subtitle Format

    Read more about it https://en.wikipedia.org/wiki/Universal_Subtitle_Format

    Example:

    with USF("path/to/file.usf") as usf:
        usf.saveSRT("file")
    """
    detect = staticmethod(detectUSF)
    read = readUSF
    save = saveUSF

    from ..development.readers import (
        # readLRC, readSAMI,
        readSRT, readSUB, 
        readTTML, readVTT
    )
