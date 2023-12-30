import io
from io import IOBase
import os
from .caption import CaptionsFormat, Block
from bs4 import BeautifulSoup


@staticmethod
def detectSAMI(content: str | io.IOBase) -> bool:
    """
    Used to detect Synchronized Accessible Media Interchange caption format.

    It returns True if:
     - the first line starts with <SAMI>
    """
    if not isinstance(content, io.IOBase):
        if not isinstance(content, str):
            raise ValueError("The content is not a unicode string or I/O stream.")
        content = io.StringIO(content)

    offset = content.tell()
    if content.readline().lstrip().startswith("<SAMI>"):
        content.seek(offset)
        return True
    content.seek(offset)
    return False


def readSAMI(self, content: str | io.IOBase, languages: list[str], **kwargs):
    content = self.checkContent(content=content, languages=languages, **kwargs)
    raise ValueError("Not Implemented")


def saveSAMI(self, filename: str, languages: list[str], **kwargs):
    filename = self.makeFilename(filename=filename, extension=self.extensions.SAMI,
                                 languages=languages, **kwargs)
    try:
        pass
    except IOError as e:
        print(f"I/O error({e.errno}): {e.strerror}")
    except Exception as e:
        print(f"Error {e}")
    raise ValueError("Not Implemented")


class SAMI(CaptionsFormat):
    """
    Synchronized Accessible Media Interchange

    Read more about it https://learn.microsoft.com/en-us/previous-versions/windows/desktop/dnacc/understanding-sami-1.0

    Example:

    with SAMI("path/to/file.sami") as sami:
        sami.saveSRT("file")
    """
    detect = staticmethod(detectSAMI)
    read = readSAMI
    save = saveSAMI

    from .srt import saveSRT
    from .sub import saveSUB
    from .ttml import saveTTML
    from .vtt import saveVTT
