import io
from .caption import CaptionsFormat, Caption

@staticmethod
def detectVTT(content: str | io.IOBase) -> bool:
    """
    Used to detect WebVTT caption format.
    
    It returns True if:
     - the first line matches `WebVTT`
    """
    if not isinstance(content, io.IOBase):
        if not isinstance(content, str):
            raise ValueError("The content is not a unicode string or I/O stream.")
        content = io.StringIO(content)

    offset = content.tell()
    if(content.readline().rstrip() == "WEBVTT"):
        content.seek(offset)
        return True
    content.seek(offset)
    return False

def readVTT(self, content: str | io.IOBase, lang: str = 'en', **kwargs):
    if not isinstance(content, io.IOBase):
        if not isinstance(content, str):
            raise ValueError("The content is not a unicode string or I/O stream.")
        content = io.StringIO(content)

def saveVTT(self, filename: str, languages: [str] = [], **kwargs):
    pass
    
class WebVTT(CaptionsFormat):
    """
    WebVTT

    Read more about it https://www.w3.org/TR/webvtt/

    Example:

    with WebVTT("path/to/file.vtt") as vtt:
        vtt.saveSRT("file")
    """
    detect = staticmethod(detectVTT)
    _read = readVTT
    save = saveVTT
   
    from .sami import saveSAMI
    from .srt import saveSRT
    from .sub import saveSUB
    from .ttml import saveTTML
