from .development.styleFormat import StyleFormat, cssParser
from .options import style_options


class FullStyle(StyleFormat):

    from .srt.style import fromSRT, getSRT
    from .sub.style import fromSUB, getSUB
    from .ttml.style import fromTTML, getTTML
    from .vtt.style import fromVTT, getVTT


class NewLinesStyle(StyleFormat):

    from .srt.style import fromSRT, getSRT
    from .sub.style import fromSUB, getSUB
    from .ttml.style import fromTTML, getTTML
    from .vtt.style import fromVTT, getVTT


class NoStyle(StyleFormat):

    from .srt.style import fromSRT, getSRT
    from .sub.style import fromSUB, getSUB
    from .ttml.style import fromTTML, getTTML
    from .vtt.style import fromVTT, getVTT


def changeStyleOption():
    if style_options.convert_style:
        Styling = FullStyle
    elif style_options.lines == -1:
        Styling = NewLinesStyle
    else:
        Styling = NoStyle


Styling = FullStyle
