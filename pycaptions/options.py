class FileExtensions:
    SRT = ".srt"
    SUB = ".sub"
    TTML = ".ttml"
    VTT = ".vtt"

    @classmethod
    def getvars(cls) -> dict:
        """
        Used to retrive all extensions for specific format.
        """
        return {attr: getattr(cls, attr) for attr in dir(cls)
                if not callable(getattr(cls, attr)) and not attr.startswith("__")}
    
save_extensions = FileExtensions()
"""
Globaly stores file extensions of implemented formats.

Example:
- Changing ttml extansion from .ttml to .xml
save_extensions.TTML = ".xml"
"""

class StyleOptions:
    convert_style = True
    convert_lines = True

style_options = StyleOptions()
