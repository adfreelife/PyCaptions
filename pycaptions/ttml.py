import io
import os
from .caption import CaptionsFormat, Block
from bs4 import BeautifulSoup


@staticmethod
def detectTTML(content: str | io.IOBase) -> bool:
    """
    Used to detect Timed Text Markup Language caption format.

    It returns True if:
     - the first line starts with `<?xml` and contains `<tt xml` OR
     - the first line starts with `<tt xml` OR
     - the second line starts with `<tt xml`
    """
    if not isinstance(content, io.IOBase):
        if not isinstance(content, str):
            raise ValueError("The content is not a unicode string or I/O stream.")
        content = io.StringIO(content)

    offset = content.tell()
    first = content.readline().lstrip()
    if (first.startswith("<tt xml") or first.startswith("<?xml") and "<tt xml" in first
        or content.readline().lstrip().startswith("<tt xml")
    ):
        content.seek(offset)
        return True
    content.seek(offset)
    return False


def readTTML(self, content: str | io.IOBase, languages: list[str], **kwargs):
    content = self.checkContent(content=content, languages=languages, **kwargs)
    raise ValueError("Not Implemented")


def saveTTML(self, filename: str, languages: list[str], **kwargs):
    filename = self.makeFilename(filename=filename, extension=self.extensions.TTML,
                                 languages=languages, **kwargs)
    try:
        pass
    except IOError as e:
        print(f"I/O error({e.errno}): {e.strerror}")
    except Exception as e:
        print(f"Error {e}")
    raise ValueError("Not Implemented")


class TTML(CaptionsFormat):
    """
    Timed Text Markup Language

    Read more about it https://www.w3.org/TR/ttml/

    Example:

    with TTML("path/to/file.ttml") as ttml:
        ttml.saveSRT("file")
    """
    detect = staticmethod(detectTTML)
    _read = readTTML
    _save = saveTTML

    from .sami import saveSAMI
    from .srt import saveSRT
    from .sub import saveSUB
    from .vtt import saveVTT
