import io
import re
from .caption import CaptionsFormat, Block, BlockType

PATTERN = r"\{.*?\}"


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
    line = content.readline()
    if re.match(r"^{\d+}{\d+}", line) or line.startswith(r"{DEFAULT}"):
        content.seek(offset)
        return True
    content.seek(offset)
    return False


def readSUB(self, content: str | io.IOBase, languages: list[str] = [], **kwargs):
    content = self.checkContent(content=content, languages=languages, **kwargs)
    languages = languages or [self.default_language]
    time_offset = kwargs.get("time_offset") or 0

    if not self.options.get("frame_rate"):
        self.options["frame_rate"] = kwargs.get("frame_rate") or 25
    frame_rate = kwargs.get("frame_rate") or self.options.get("frame_rate")

    if not self.options.get("blocks"):
        self.options["blocks"] = []

    line = content.readline().strip()
    while line:
        if line.startswith(r"{DEFAULT}"):
            self.options["blocks"].append(Block(BlockType.STYLE, style=line))
        else:
            lines = line.split("|")
            params = re.findall(PATTERN, lines[0])
            start = _convertFromSUBTime(params[0].strip("{}"), frame_rate)
            end = _convertFromSUBTime(params[1].strip("{}"), frame_rate)
            caption = Block(BlockType.CAPTION, start_time=start, end_time=end,
                            style=[p.strip("{}") for p in params[2:]])
            for counter, line in enumerate(lines):
                if len(languages) > 1:
                    caption.append(re.sub(PATTERN, "", line), languages[counter])
                else:
                    caption.append(re.sub(PATTERN, "", line), languages[0])
            caption.shift_time(time_offset)
            self.append(caption)
        line = content.readline().strip()


def _convertFromSUBTime(time: str, frame_rate: int):
    return int(time) * 1_000_000 / frame_rate


def _convertToSUBTime(time: int, frame_rate: int):
    return int(time * frame_rate / 1_000_000)


def saveSUB(self, filename: str, languages: list[str] = [], **kwargs):
    filename = self.makeFilename(filename=filename, extension=self.extensions.SUB,
                                 languages=languages, **kwargs)
    languages = languages or [self.default_language]
    frame_rate = kwargs.get("frame_rate") or self.options.get("frame_rate") or 25
    encoding = kwargs.get("file_encoding") or "UTF-8"
    try:
        with open(filename, "w", encoding=encoding) as file:
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
    detect = staticmethod(detectSUB)
    _read = readSUB
    _save = saveSUB

    from .sami import saveSAMI
    from .srt import saveSRT
    from .ttml import saveTTML
    from .vtt import saveVTT
