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


def readSRT(self, content: str | io.IOBase, languages: list[str], **kwargs):
    content = self.checkContent(content=content, languages=languages, **kwargs)
    content.readline()
    start, end = content.readline().split("-->")
    start = _convertFromSRTTime(start)
    end = _convertFromSRTTime(end)
    line = content.readline()
    caption = Block(BlockType.CAPTION, languages[0], start, end, line)
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
            caption = Block(BlockType.CAPTION, languages[0], start, end, line)
        else:
            if len(languages) > 1:
                caption.append(line, languages[counter])
                counter += 1
            else:
                caption.append(line, languages[0])
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
    return f"{hours:02}:{minutes:02}:{seconds:02},{miliseconds:03}"


def saveSRT(self, filename: str, languages: list[str], **kwargs):
    filename = self.makeFilename(filename=filename, extension=self.extensions.SRT,
                                 languages=languages, **kwargs)
    try:
        with open(filename, "w", encoding="UTF-8") as file:
            index = 1
            for i, data in enumerate(self):
                if data.block_type != BlockType.CAPTION:
                    continue
                file.write(f"{index}\n")
                file.write(f"{_convertToSRTTime(data.start_time)} --> {_convertToSRTTime(data.end_time)}\n")
                file.write("\n".join(data.get(i) for i in languages))
                if i != len(self)-1:
                    file.write("\n\n")
                index += 1
    except IOError as e:
        print(f"I/O error({e.errno}): {e.strerror}")
    except Exception as e:
        print(f"Error {e}")


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
    read = readSRT
    save = saveSRT

    from .sami import saveSAMI
    from .sub import saveSUB
    from .ttml import saveTTML
    from .vtt import saveVTT
