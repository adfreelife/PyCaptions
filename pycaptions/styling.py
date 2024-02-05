from .styleFormat import StyleFormat, cssParser
from .options import style_options

class Styling(StyleFormat):

    from .srt.style import fromSRT, getSRT
    from .sub.style import fromSUB, getSUB
    from .ttml.style import fromTTML, getTTML
    from .vtt.style import fromVTT, getVTT
