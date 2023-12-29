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


def readSUB(self, content: str | io.IOBase, languages: list[str] = [], **kwargs):
    content = self.checkContent(content=content, languages=languages, **kwargs)
    frame_rate = kwargs.get("frame_rate") or 25
    raise ValueError("Not Implemented")


def saveSUB(self, filename: str, languages: list[str] = [], **kwargs):
    filename = self.makeFilename(filename=filename, extension=self.extensions.SUB,
                                 languages=languages, **kwargs)
    try:
        pass
    except IOError as e:
        print(f"I/O error({e.errno}): {e.strerror}")
    except Exception as e:
        print(f"Error {e}")
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
