import io
from .caption import CaptionsFormat, Block, BlockType

EXTENSION = ".srt"


@staticmethod
def detectSRT(content: str | io.IOBase) -> bool:
    """
    Used to detect SubRip caption format.

    It returns True if:
     - the first line is a number 1
     - the second line contains a `-->`
    """
    if not isinstance(content, io.IOBase):
        if not isinstance(content, str):
            raise ValueError("The content is not a unicode string or I/O stream.")
        content = io.StringIO(content)

    offset = content.tell()
    if content.readline().rstrip() == "1" and '-->' in content.readline():
        content.seek(offset)
        return True
    content.seek(offset)
    return False


def readSRT(self, content: str | io.IOBase, lang: list[str] = None, **kwargs):
    content.readline()
    start, end = content.readline().split("-->")
    start = _convertFromSRTTime(start)
    end = _convertFromSRTTime(end)
    line = content.readline()
    caption = Block(BlockType.CAPTION, lang[0], start, end, line)
    counter = 1
    while line:
        if not line.strip():
            counter = 1
            self.append(caption)
            content.readline()
            start, end = content.readline().split("-->")
            start = _convertFromSRTTime(start)
            end = _convertFromSRTTime(end)
            line = content.readline()
            caption = Block(BlockType.CAPTION, lang[0], start, end, line)
        else:
            if len(lang) > 1:
                caption.append(line, lang[counter])
                counter += 1
            else:
                caption.append(line, lang[0])
        line = content.readline()
    self.append(caption)


def _convertFromSRTTime(time: str) -> int:
    time = time.strip()
    return (int(time[0:2])*3_600_000_000 +
            int(time[3:5])*60_000_000 +
            int(time[6:8])*1_000_000 +
            int(time[9:])*1_000)


def _convertToSRTTime(time: int) -> str:
    hours, reminder = divmod(time, 3_600_000_000)
    minutes, reminder = divmod(reminder, 60_000_000)
    seconds, miliseconds = divmod(reminder, 1_000_000)
    miliseconds = int(miliseconds/1_000)
    return f"{hours}:{minutes}:{seconds},{miliseconds}"


def saveSRT(self, filename: str, languages: [str] = [], **kwargs):
    with open(filename, "w", encoding="UTF-8") as file:
        index = 1
        for data in self.caption_list:
            if data.block_type != BlockType.CAPTION:
                continue
            file.write(f"{index}\n")
            file.write(f"{_convertToSRTTime(data.start_time)} --> {_convertToSRTTime(data.end_time)}\n")
            file.write("\n".join(data.get(i) for i in languages))
            file.write("\n")
            index += 1


class SubRip(CaptionsFormat):
    """
    SubRip

    Read more about it https://en.wikipedia.org/wiki/SubRip

    Example:

    with SubRip("path/to/file.srt") as srt:
        srt.saveVTT("file")
    """
    EXTENSION = EXTENSION
    detect = staticmethod(detectSRT)
    _read = readSRT
    _save = saveSRT

    from .sami import saveSAMI
    from .sub import saveSUB
    from .ttml import saveTTML
    from .vtt import saveVTT
