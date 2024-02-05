from .development.styleFormat import StyleFormat, cssParser


class FullStyle(StyleFormat):

    from .srt.style import fromSRT, getSRT
    from .sub.style import fromSUB, getSUB
    from .ttml.style import fromTTML, getTTML
    from .vtt.style import fromVTT, getVTT


class NewLinesStyle(StyleFormat):

    from .srt.style import fromSRTLine as fromSRT, getSRTLine as getSRT
    from .sub.style import fromSUBLine as fromSUB, getSUBLine as getSUB
    from .ttml.style import fromTTMLLine as fromTTML, getTTMLLine as getTTML
    from .vtt.style import fromVTTLine as fromVTT, getVTTLine as getVTT


class NoStyle(StyleFormat):

    from .srt.style import fromSRT, getSRT
    from .sub.style import fromSUB, getSUB
    from .ttml.style import fromTTML, getTTML
    from .vtt.style import fromVTT, getVTT


def changeStyleOption(style, lines):
    if style == "full":
        Styling = FullStyle
    elif lines == -1:
        Styling = NewLinesStyle
    else:
        Styling = NoStyle


Styling = FullStyle
