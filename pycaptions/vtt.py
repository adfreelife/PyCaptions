import io
import re
from .caption import CaptionsFormat, Block, BlockType
from cssutils import CSSParser

STYLE_PATERN = re.compile(r"::cue\((#[^)]+)\)")


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
    if content.readline().rstrip().startswith("WEBVTT"):
        content.seek(offset)
        return True
    content.seek(offset)
    return False


def readVTT(self, content: str | io.IOBase, languages: list[str], **kwargs):
    content = self.checkContent(content=content, languages=languages, **kwargs)
    global STYLE_PATERN

    self.options["blocks"] = []
    metadata = Block(BlockType.METADATA)
    content.readline()
    line = content.readline().strip()
    while line:
        line = line.split(": ", 1)
        metadata.options[line[0]] = line[1]
        line = content.readline().strip()
    self.options["blocks"].append(metadata)

    self.options["style"] = dict()
    self.options["style"]["identifier_to_original"] = dict()
    self.options["style"]["identifier_to_new"] = dict()
    self.options["style"]["style_id_counter"] = 0

    line = content.readline()
    while line:
        line = line.strip()
        if line.startswith("NOTE"):
            temp = line.split(" ", 1)
            comment = Block(BlockType.COMMENT)
            if len(temp) > 1:
                comment.append(temp[1])
            line = content.readline().strip()
            while line:
                comment.append(line)
                line = content.readline().strip()
            self.options["blocks"].append(comment)
        elif line == "STYLE":
            style = ""
            line = content.readline().strip()
            while line:
                style += line
                line = content.readline().strip()

            def replace_style(match):
                if match.group(1).startswith("#"):
                    if match.group(1) in self.options["style"]["identifier_to_new"]:
                        return self.options["style"]["identifier_to_new"][match.group(1)]
                    self.options["style"]["style_id_counter"] += 1
                    style_name = f"#style{self.options['style']['style_id_counter']}"
                    self.options["style"]["identifier_to_original"][style_name] = match.group(1)
                    self.options["style"]["identifier_to_new"][match.group(1)] = style_name
                    return style_name
                return match.group(1)
            parser = CSSParser(validate=False)
            style = parser.parseString(
                        cssText=re.sub(STYLE_PATERN, replace_style, style),
                        encoding="UTF-8"
                    )
            self.options["blocks"].append(Block(BlockType.STYLE, style=style))
        elif line == "REGION":
            line = content.readline().strip()
            temp = dict()
            while line:
                line = line.split(":", 1)
                temp[line[0]] = line[1]
                line = content.readline().strip()
            self.options["blocks"].append(Block(BlockType.LAYOUT, layout=temp))
        else:
            break
        line = content.readline()

    while line:
        if line.startswith("NOTE"):
            temp = line.split(" ", 1)
            comment = Block(BlockType.COMMENT)
            if len(temp) > 1:
                comment.append(temp[1])
            line = content.readline().strip()
            while line:
                comment.append(line)
                line = content.readline().strip()
            self.append(comment)
        else:
            caption = Block(BlockType.CAPTION)
            if "-->" not in line:
                caption.options["indentificator"] = line.strip()
                line = content.readline().strip()
            start, end = line.split(" --> ", 1)
            end = end.split(" ", 1)
            if len(end) > 1:
                caption.options["style"] = end[1]
            end = end[0]
            caption.start_time = _convertFromVTTTime(start)
            caption.end_time = _convertFromVTTTime(end)
            counter = 1
            line = content.readline().strip()
            if line.startswith("{"):
                caption.block_type = BlockType.METADATA
            while line:
                if len(languages) > 1:
                    caption.append(line, languages[counter])
                    counter += 1
                else:
                    caption.append(line, languages[0])
                line = content.readline().strip()
            self.append(caption)
        line = content.readline()


def _convertFromVTTTime(time: str) -> int:
    converter = [1_000_000, 60_000_000, 3_600_000_000]
    return int(time[-3:])*1_000+sum(int(t)*c for t, c in zip(reversed(time[:-4].split(":")), converter))


def _convertToVTTTime(time: int) -> str:
    hours, reminder = divmod(time, 3_600_000_000)
    minutes, reminder = divmod(reminder, 60_000_000)
    seconds, miliseconds = divmod(reminder, 1_000_000)
    miliseconds = int(miliseconds/1_000)
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}.{int(miliseconds):03}"


def saveVTT(self, filename: str, languages: list[str], **kwargs):
    filename = self.makeFilename(filename=filename, extension=self.extensions.VTT,
                                 languages=languages, **kwargs)
    try:
        pass
    except IOError as e:
        print(f"I/O error({e.errno}): {e.strerror}")
    except Exception as e:
        print(f"Error {e}")
    raise ValueError("Not Implemented")


class WebVTT(CaptionsFormat):
    """
    Web Video Text Tracks

    Read more about it: https://www.speechpad.com/captions/webvtt
    Full specification: https://www.w3.org/TR/webvtt/

    Example:

    with WebVTT("path/to/file.vtt") as vtt:
        vtt.saveSRT("file")
    """
    detect = staticmethod(detectVTT)
    _read = readVTT
    _save = saveVTT

    from .sami import saveSAMI
    from .srt import saveSRT
    from .sub import saveSUB
    from .ttml import saveTTML
