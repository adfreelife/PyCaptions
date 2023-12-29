import io
import re
from .caption import CaptionsFormat, Block, BlockType
from cssutils import CSSParser

EXTENSION = ".vtt"
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
    if(content.readline().rstrip() == "WEBVTT"):
        content.seek(offset)
        return True
    content.seek(offset)
    return False


def readVTT(self, content: str | io.IOBase, lang: str = 'en', **kwargs):
    global STYLE_PATERN
    if not isinstance(content, io.IOBase):
        if not isinstance(content, str):
            raise ValueError("The content is not a unicode string or I/O stream.")
        content = io.StringIO(content)

    content.readline()
    line = content.readline().strip()
    self.options["blocks"] = []
    metadata = Block(BlockType.METADATA, lang)
    while line:
        line = line.split(": ",1)
        metadata.options[line[0]] = line[1]
        line = content.readline().strip()
    self.options["blocks"].append(metadata)

    comment_count = 0
    line = content.readline()
    self.options["style"] = dict()
    self.options["style"]["styles"] = []
    self.options["style"]["identifier_to_original"] = dict()
    self.options["style"]["identifier_to_new"] = dict() 
    self.options["style"]["style_id_counter"] = 0

    while line:
        if line.startswith("NOTE"):
            comment_count+=1
            temp = line.split(" ",1)
            comment = Block(BlockType.COMMENT, lang)
            if len(temp) > 1:
                comment.append(temp[1],lang)
            line = line.readline().strip()
            while line:
                comment.append(line,lang)
                line = line.readline().strip()
            self.options["blocks"].append(comment)
        elif line == "STYLE":
            style = ""
            line = line.readline().strip()
            parser = CSSParser(validate=False)
            while line:
                style += line  
                line = line.readline().strip()

            def replace_style(match):
                if match.group(1).startswith("#"):
                    if match.group(1) not in self.options["style"]["identifier_to_new"]:
                        return self.options["style"]["identifier_to_new"][match.group(1)]
                    self.options["style"]["style_id_counter"] += 1
                    style_name = f"#style{self.options['style']['style_id_counter']}"
                    self.options["style"]["identifier_to_original"][style_name] = match.group(1)
                    self.options["style"]["identifier_to_new"][match.group(1)] = style_name
                    return style_name
                return match.group(1)
            self.options["style"]["styles"].append({"order":counter, "style":
                parser.parseString(cssText=re.sub(STYLE_PATERN, replace_style, style), encoding="UTF-8")})
        elif line == "REGION":
            line = line.readline().strip()
            temp = dict()
            while line:
                line = line.split(":",1)
                temp[line[0]] = line[1]
                line = line.readline().strip()
            self.options["layout"].append({"order":counter, "layout":temp})
        else:
            break
        line = content.readline()

    while line:
        line = line.strip()
        if line.startswith("NOTE"):
            temp = line.split(" ",1)
            comment = []
            if len(temp) > 1:
                comment.append[temp[1]]
            line = line.readline().strip()
            while line:
                comment.append(line)
                line = line.readline().strip()
        else:
            pass
        line = content.readline()


def saveVTT(self, filename: str, languages: [str] = [], **kwargs):
    pass


class WebVTT(CaptionsFormat):
    """
    Web Video Text Tracks

    Read more about it: https://www.speechpad.com/captions/webvtt
    Full specification: https://www.w3.org/TR/webvtt/

    Example:

    with WebVTT("path/to/file.vtt") as vtt:
        vtt.saveSRT("file")
    """
    EXTENSION = EXTENSION
    detect = staticmethod(detectVTT)
    _read = readVTT
    _save = saveVTT

    from .sami import saveSAMI
    from .srt import saveSRT
    from .sub import saveSUB
    from .ttml import saveTTML
