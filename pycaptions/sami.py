import io, os
from .caption import CaptionsFormat, Block
from bs4 import BeautifulSoup

EXTENSION = ".sami"

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
    if(content.readline().lstrip().startswith("<SAMI>")):
        content.seek(offset)
        return True
    content.seek(offset)
    return False
    
def readSAMI(self, content: str | io.IOBase, lang: str = 'en', **kwargs):
    if not isinstance(content, io.IOBase):
        if not not isinstance(content, str):
            raise ValueError("The content is not a unicode string or I/O stream.")
        content = io.StringIO(content)
    raise ValueError("Not Implemented")

def saveSAMI(self, filename: str, languages: [str] = [], **kwargs):
    languages = languages or [self.default_language]
    if not filename.endswith(".sami"):
        filename += ".sami"

    for i in languages:
        if i not in filename:
            file, ext = os.path.splitext(filename)
            filename = f"{file}.{i}{ext}"
    raise ValueError("Not Implemented")
    

class SAMI(CaptionsFormat):
    """
    Synchronized Accessible Media Interchange

    Read more about it https://learn.microsoft.com/en-us/previous-versions/windows/desktop/dnacc/understanding-sami-1.0

    Example:

    with SAMI("path/to/file.sami") as sami:
        sami.saveSRT("file")
    """
    EXTENSION = EXTENSION
    detect = staticmethod(detectSAMI)
    _read = readSAMI
    _save = saveSAMI

    from .srt import saveSRT
    from .sub import saveSUB
    from .ttml import saveTTML
    from .vtt import saveVTT