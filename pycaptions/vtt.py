import io
from .caption import CaptionsFormat, Caption
from cssutils import CSSParser

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

    content.readline()
    line = content.readline().strip()
    self.options["metadata"] = dict()
    while line:
        line = line.split(": ",1)
        self.options["metadata"][line[0]] = line[1]
        line = content.readline().strip()

    comment_count = 0
    counter = 1
    line = content.readline()
    self.options["comments"] = []
    self.options["style"] = {}
    self.options["layout"] = {}
    while line:
        if line.startswith("NOTE"):
            comment_count+=1
            temp = line.split(" ",1)
            comment = []
            if len(temp) > 1:
                comment.append[temp[1]]
            line = line.readline().strip()
            while line:
                comment.append(line)
                line = line.readline().strip()
            self.options["comments"].append({"line":counter, "comment": comment})
        elif line == "STYLE":
            style = ""
            line = line.readline().strip()
            parser = CSSParser(validate=False)
            while line:
                style += line  
                line = line.readline().strip()
            parser.parseString(cssText=style, encoding="UTF-8")

        elif line == "REGION":
            line = line.readline().strip()
            while line:
                comment.append(line)
                line = line.readline().strip()
        else:
            break
        counter+=1
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
    detect = staticmethod(detectVTT)
    _read = readVTT
    save = saveVTT
   
    from .sami import saveSAMI
    from .srt import saveSRT
    from .sub import saveSUB
    from .ttml import saveTTML
