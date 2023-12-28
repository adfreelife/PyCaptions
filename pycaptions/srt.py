import io, os
from typing import NoReturn
from .caption import CaptionsFormat, Caption

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
    if(content.readline().rstrip() == "1" and '-->' in content.readline()):
        content.seek(offset)
        return True
    content.seek(offset)
    return False
        
def readSRT(self, content: str | io.IOBase, lang: str = None, **kwargs):
    lang = lang or self.default_language
    if not isinstance(content, io.IOBase):
        if not isinstance(content, str):
            raise ValueError("The content is not a unicode string or I/O stream.")
        content = io.StringIO(content)
    content.readline()
    start, end = content.readline().split("-->")
    start = _convertFromSRTTime(start)
    end = _convertFromSRTTime(end)
    line = content.readline()
    caption = Caption(lang, start, end, line)
    while line:
        if not line.strip():
            self.append(caption)
            content.readline()
            start, end = content.readline().split("-->")
            start = _convertFromSRTTime(start)
            end = _convertFromSRTTime(end)
            line = content.readline()
            caption = Caption(lang, start, end, line)
        else:
            caption.append(line, lang)
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
    seconds, miliseconds = divmod(reminder,1_000_000)
    miliseconds = int(miliseconds/1_000)
    return f"{hours}:{minutes}:{seconds},{miliseconds}"

def saveSRT(self, filename: str, languages: [str] = [], **kwargs):
    languages = languages or [self.default_language]
    if not filename.endswith(".srt"):
        filename += ".srt"

    for i in languages:
        if i not in filename:
            file, ext = os.path.splitext(filename)
            filename = f"{file}.{i}{ext}"
    
    try:
        with open(filename,"w",encoding="UTF-8") as file:
            for index, data in enumerate(self.caption_list, 1):
                file.write(f"{index}\n")
                file.write(f"{_convertToSRTTime(data.start_time)} --> {_convertToSRTTime(data.end_time)}\n")
                for i in languages:
                    file.writable("\n".join(data.get(i)))
                file.write("\n")
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
    _read = readSRT
    save = saveSRT

    from .sami import saveSAMI
    from .sub import saveSUB
    from .ttml import saveTTML
    from .vtt import saveVTT

if __name__ == "__main__":
    srt = SubRip()
    with open("tests/test.en.srt", encoding="UTF-8") as file:
        if(srt.detect(file)):
            srt.read(file)