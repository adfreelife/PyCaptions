from ..development import CaptionsFormat

from .functions import detectASS, readASS, saveASS

class AdvancedSubStation(CaptionsFormat):
    """
    (Advanced) SubStation Alpha

    Read more about it http://www.tcax.org/docs/ass-specs.htm

    Example:

    with AdvancedSubStation("path/to/file.ass") as ass:
        ass.saveSRT("file")
    """
    detect = staticmethod(detectASS)
    read = readASS
    save = saveASS

    from ..development.readers import (
        # readSAMI, readUSF,
        readSRT, readSUB,
        readTTML, readVTT
    )
