import io
import re
import os
from .caption import CaptionsFormat, Block

EXTENSION = ".sub"


@staticmethod
def detectSUB(content: str | io.IOBase) -> bool:
    r"""
    Used to detect MicroDVD caption format.

    It returns True if:
     - the start of a first line in a file matches regex `^{\d+}{\d+}`
    """
    if not isinstance(content, io.IOBase):
        if not isinstance(content, str):
            raise ValueError("The content is not a unicode string or I/O stream.")
        content = io.StringIO(content)

    offset = content.tell()
    if re.match(r"^{\d+}{\d+}", content.readline()):
        content.seek(offset)
        return True
    content.seek(offset)
    return False


def readSUB(self, content: str | io.IOBase, lang: str = 'en', **kwargs):
    frame_rate = kwargs.get("frame_rate") or 25
    if not isinstance(content, io.IOBase):
        if not isinstance(content, str):
            raise ValueError("The content is not a unicode string or I/O stream.")
        content = io.StringIO(content)
    raise ValueError("Not Implemented")


def saveSUB(self, filename: str, languages: [str] = [], **kwargs):
    raise ValueError("Not Implemented")


class MicroDVD(CaptionsFormat):
    """
    MicroDVD

    Read more about it https://en.wikipedia.org/wiki/MicroDVD

    Example:

    with MicroDVD("path/to/file.sub") as sub:
        sub.saveSRT("file")
    """
    EXTENSION = EXTENSION
    detect = staticmethod(detectSUB)
    _read = readSUB
    _save = saveSUB

    from .sami import saveSAMI
    from .srt import saveSRT
    from .ttml import saveTTML
    from .vtt import saveVTT
