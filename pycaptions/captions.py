import io
from .caption import CaptionsFormat

class Captions(CaptionsFormat):
    """
    Captions

    A generic class to read different types of caption formats.

    Example:

    with Captions("path/to/file.srt") as captions:
        captions.saveSRT("file")
    """
    def __init__(self, filename: str = None, default_language: str = "und", **options):
        self.fileFormat = "srt"
        super().__init__(filename, default_language, **options)
    
    from .sami import detectSAMI, saveSAMI, readSAMI, EXTENSION as sami_extension
    from .srt import detectSRT, saveSRT, readSRT, EXTENSION as srt_extension
    from .sub import detectSUB, saveSUB, readSUB, EXTENSION as sub_extension
    from .ttml import detectTTML, saveTTML, readTTML, EXTENSION as ttml_extension
    from .vtt import detectVTT, saveVTT, readVTT, EXTENSION as vtt_extension

    extensions = {
        "sami": sami_extension,
        "srt": srt_extension,
        "sub": sub_extension,
        "ttml": ttml_extension,
        "vtt": vtt_extension
    }

    def getExtension(self):
        return self.extensions[self.fileFormat]

    readers = {
        "sami" : readSAMI,
        "srt" : readSRT,
        "sub" : readSUB,
        "ttml" : readTTML,
        "vtt" : readVTT
    }

    savers = {
        "sami" : saveSAMI,
        "srt" : saveSRT,
        "sub" : saveSUB,
        "ttml" : saveTTML,
        "vtt" : saveVTT
    }

    def get_format(self, file: str | io.IOBase) -> str | None:
        if self.detectSAMI(file):
            self.fileFormat = "sami"
        if self.detectSRT(file):
            self.fileFormat = "srt"
        if self.detectSUB(file):
            self.fileFormat = "sub"
        if self.detectTTML(file):
            self.fileFormat = "ttml"
        if self.detectVTT(file):
            self.fileFormat = "vtt"
        return self.fileFormat
    
    def detect(self, content: str | io.IOBase) -> bool:
        if not self.get_format(content):
            return False
        return True
    
    def _read(self, content: str | io.IOBase, lang: str = None, **kwargs):
        self.readers[self.fileFormat](self, content, lang, **kwargs)
    
    def read(self, content: str | io.IOBase, lang: str = None, **kwargs):
        format = self.get_format(content)
        if not format:
            return
        self.readers[format](self, content, lang, **kwargs)

    def save(self, filename: str, format: str = "srt", lang: str = None, **kwargs):
        self.savers[format](self, filename, lang, **kwargs)