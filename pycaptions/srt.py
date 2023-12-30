import io
from .caption import CaptionsFormat, Block, BlockType


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
    languages = languages or [self.default_language]
    time_offset = kwargs.get("time_offset") or 0

    counter = 1
    line = content.readline()
    while line:
        start, end = content.readline().split(" --> ")
        caption = Block(BlockType.CAPTION, languages[0], _convertFromSRTTime(start),
                        _convertFromSRTTime(end), content.readline().strip())
        line = content.readline().strip()
        while line:
            if len(languages) > 1:
                caption.append(line, languages[counter])
                counter += 1
            else:
                caption.append(line, languages[0])
            line = content.readline().strip()
        caption.shift_time(time_offset)
        self.append(caption)
        line = content.readline()


def _convertFromSRTTime(time: str) -> int:
    return (int(time[0:2])*3_600_000_000 +
            int(time[3:5])*60_000_000 +
            int(time[6:8])*1_000_000 +
            int(time[9:])*1_000)


def _convertToSRTTime(time: int) -> str:
    hours, reminder = divmod(time, 3_600_000_000)
    minutes, reminder = divmod(reminder, 60_000_000)
    seconds, miliseconds = divmod(reminder, 1_000_000)
    miliseconds = int(miliseconds/1_000)
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02},{int(miliseconds):03}"


def saveSRT(self, filename: str, languages: list[str], **kwargs):
    filename = self.makeFilename(filename=filename, extension=self.extensions.SRT,
                                 languages=languages, **kwargs)
    encoding = kwargs.get("file_encoding") or "UTF-8"
    languages = languages or [self.default_language]
    try:
        with open(filename, "w", encoding=encoding) as file:
            index = 1
            for data in self:
                if data.block_type != BlockType.CAPTION:
                    continue
                elif index != 1:
                    file.write("\n\n")
                file.write(f"{index}\n")
                file.write(f"{_convertToSRTTime(data.start_time)} --> {_convertToSRTTime(data.end_time)}\n")
                file.write("\n".join(data.get(i) for i in languages))
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
    detect = staticmethod(detectSRT)
    read = readSRT
    save = saveSRT

    from .sami import saveSAMI
    from .sub import saveSUB
    from .ttml import saveTTML
    from .vtt import saveVTT
