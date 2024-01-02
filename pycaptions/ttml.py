import io
import os

from .block import Block, BlockType
from .captionsFormat import CaptionsFormat
from .microTime import MicroTime as MT
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

# ttp:frameRate, ttp:frameRateMultiplier, ttp:subFrameRate, ttp:tickRate, ttp:timeBase
def readTTML(self, content: str | io.IOBase, languages: list[str], **kwargs):
    content = self.checkContent(content=content, languages=languages, **kwargs)
    languages = languages or [self.default_language]
    time_offset = kwargs.get("time_offset") or 0
    content = BeautifulSoup(content, "xml")
    for langs in content.body.find_all("div"):
        lang = langs.get("xml:lang")
        p_start, p_end = MT.fromTTMLTime(langs.get("begin"), langs.get("dur"), langs.get("end"))
        for i in langs.find_all("p"):
            start, end = MT.fromTTMLTime(i.get("begin"), i.get("dur"), i.get("end"))
            start += p_start
            if start > p_end:
                start = p_end
                end = p_end
            elif end > p_end:
                end = p_end
            caption = Block(BlockType.CAPTION, lang or languages[0], start, end)
            for line in i.get_text().split("\n"):
                caption.append(line, lang or languages[0])
            caption.shift_time(time_offset)
            self.append(caption)


def saveTTML(self, filename: str, languages: list[str] = None, **kwargs):
    filename = self.makeFilename(filename=filename, extension=self.extensions.TTML,
                                 languages=languages, **kwargs)
    encoding = kwargs.get("file_encoding") or "UTF-8"
    languages = languages or [self.default_language]
    try:
        with open(filename, "w", encoding=encoding) as file:
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
