from ..development import CaptionsFormat

from .functions import detectSRT, readSRT, saveSRT


class SubRip(CaptionsFormat):
    """
    SubRip

    Read more about it https://en.wikipedia.org/wiki/SubRip

    Example:

    with SubRip("path/to/file.srt") as srt:
        srt.saveVTT("file")
    """
    detect = staticmethod(detectSRT)
    read = readSRT
    save = saveSRT

    from ..development.readers import (
        # readLRC, readSAMI, readUSF,
        readSUB, readTTML, readVTT
    )
