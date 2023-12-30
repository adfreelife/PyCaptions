import json
import textwrap
import budoux
import io
import os
from collections import defaultdict
from langcodes import standardize_tag, tag_is_valid


class BlockType:
    CAPTION = 1
    COMMENT = 2
    STYLE = 3
    LAYOUT = 4
    METADATA = 5


class FileExtensions:
    SAMI = ".sami"
    SRT = ".srt"
    SUB = ".sub"
    TTML = ".ttml"
    VTT = ".vtt"


class Block:
    """
    Represents a block of content in a multimedia file or document.

    Methods:
        getLines: Format text of specific language into multiple lines
        get: Get the text content of the block for a specific language.
        append: Append text to the block for a specific language.
        shift_time: Shift start and end times of the block by a specified duration.
        shift_start: Shift start time of the block by a specified duration.
        shif_end: Shift end time of the block by a specified duration.
        copy: Returns a copy of the current block.
        shift_time_us: Shift time of the block by microseconds.
        shift_start_us: Shift start time of the block by microseconds.
        shift_end_us: Shift end time of the block by microseconds.
        __getitem__: Retrieve the text of specific language.
        __setitem__: Set the text of specific language.
        __str__: Return a string representation of the block.
        __iadd__: In-place addition for the Block.
        __add__: Addition for the Blocks.
        __isub__: In-place subtraction for a specific language.
        __sub__: Subtraction for a specific language.
        __iter__: Iterator for iterating through the block languages.
        __next__: Iterator method returning a tuple of language and text.
    """
    def __init__(self, block_type: int, lang: str = "und", start_time: int = 0,
                 end_time: int = 0, text: str = "", **options):
        """
        Initialize a new instance of the Block class.

        Parameters:
        - block_type (int): The type of the block, represented as an integer, options in BlockType class
        - lang (str, optional): The language of the text in the block (default is "und" for undefined).
        - start_time (int, optional): The starting time of the block in microseconds (default is 0).
        - end_time (int, optional): The ending time of the block in microseconds (default is 0).
        - text (str, optional): The content of the block (default is an empty string).
        - **options: Additional keyword arguments for customization (e.g style, layout, ...).
        """
        self.block_type = block_type
        self.languages = defaultdict(str)
        if options.get("languages"):
            for i, j in options.get("languages").items():
                self.languages[i] = j
            del options["languages"]
        self.default_language = lang
        if text:
            self.languages[lang] = text.strip()
        self.start_time = start_time
        self.end_time = end_time
        self.options = options or {}
    
    def __getitem__(self, index: str):
        return self.languages[index]

    def __setitem__(self, index: str, value: str):
        self.languages[index] = value

    def __str__(self):
        temp = '\n'.join(f" {lang}: {text}" for lang, text in self.languages.items())
        return f"start: {self.start_time} end: {self.end_time}\n{temp}"

    def __iadd__(self, value):
        if not isinstance(value, Block):
            raise ValueError("Unsupported type. Must be an instance of `Block`")
        for key, language in value:
            self.languages[key] = language
        return self

    def __add__(self, value):
        if not isinstance(value, Block):
            raise ValueError("Unsupported type. Must be an instance of `Block`")
        out = Block(block_type=self.block_type, start_time=self.start_time,
                    end_time=self.end_time, lang=self.default_language, options=self.options)
        out.languages = self.languages.copy()
        for key, language, comment in value:
            out.languages[key] = language
        return out

    def __isub__(self, language: str):
        if language in self.languages:
            del self.languages[language]
        return self

    def __sub__(self, language: str):
        out = Block(block_type=self.block_type, start_time=self.start_time,
                    end_time=self.end_time, lang=self.default_language, options=self.options)
        out.languages = self.languages.copy()
        if language in out.languages:
            del out.languages[language]
        return out

    def __iter__(self):
        self._keys_iterator = iter(self.languages)
        return self

    def __next__(self):
        try:
            key = next(self._keys_iterator)
            return key, self.languages.get(key)
        except StopIteration:
            raise StopIteration

    def copy(self):
        return Block(self.block_type, self.default_language, self.start_time,
                     self.end_time, languages=self.languages, **self.options)

    def getLines(self, lang: str = "und", lines: int = 0) -> list[str]:
        """
        Format text of specific language into multiple lines.

        Args:
            lang (str, optional): Language code (default is "und" for undefined).
            lines (int, optional): The number of lines to format to. (default is 0 - autoformat).

        Returns:
            list[str]: A list of text lines.
        """
        text = self.get(lang)
        if lang == "ja":
            parser = budoux.load_default_japanese_parser()
            return parser.parse(text)
        elif lang in ["zh", "zh-CN", "zh-SG", "zh-Hans"]:
            parser = budoux.load_default_simplified_chinese_parser()
            return parser.parse(text)
        elif lang in ["zh-HK", "zh-MO", "zh-TW", "zh-Hant"]:
            parser = budoux.load_default_simplified_chinese_parser()
            return parser.parse(text)
        else:
            return textwrap.wrap(text)

    def get(self, lang: str) -> str:
        return self.languages.get(lang)

    def append(self, text: str, lang: str = "und"):
        if not self.default_language:
            self.default_language = lang
        if lang not in ["ja", "zh", "zh-CN", "zh-SG", "zh-Hans",
                        "zh-HK", "zh-MO", "zh-TW", "zh-Hant"]:
            if self.languages[lang]:
                self.languages[lang] += " " + text.strip()
            else:
                self.languages[lang] = text.strip()
        else:
            self.languages[lang] += text

    def get_microseconds(self, microseconds: int, miliseconds: int = 0, seconds: int = 0,
                         minutes: int = 0, hours: int = 0):
        return (microseconds + miliseconds * 1_000 + seconds * 1_000_000 +
                minutes * 60_000_000 + hours * 3_600_000_000)

    def shift_time_us(self, microseconds: int):
        self.start_time += microseconds
        self.end_time += microseconds

    def shift_time(self, microseconds: int, miliseconds: int = 0, seconds: int = 0,
                   minutes: int = 0, hours: int = 0):
        self.shift_time_us(self.get_microseconds(microseconds, miliseconds, seconds, minutes, hours))

    def shift_start_us(self, microseconds: int):
        self.start_time += microseconds

    def shift_start(self, microseconds: int, miliseconds: int = 0, seconds: int = 0,
                    minutes: int = 0, hours: int = 0):
        self.start_time += self.get_microseconds(microseconds, miliseconds, seconds, minutes, hours)

    def shift_end_us(self, microseconds: int):
        self.end_time += microseconds

    def shift_end(self, microseconds, miliseconds: int = 0, seconds: int = 0,
                  minutes: int = 0, hours: int = 0):
        self.end_time += self.get_microseconds(microseconds, miliseconds, seconds, minutes, hours)


class CaptionsFormat:
    """
    Represents a format for handling captions in a multimedia context.

    Attributes:
        extensions (FileExtensions): An instance of the FileExtensions class for managing file extensions.

     Methods:
        setDefaultLanguage: Set the default language for captions.
        insert: Insert a block at the specified index.
        detect: Detect the format of the captions file.
        read: Read captions from content.
        checkContent: Check if the content is valid type.
        save: Save captions to a file.
        makeFilename: Adds languages and extension to filename.
        append: Append a Block to the list of blocks.
        shift_time: Shift the timing of all blocks by the specified duration.
        shift_start: Shift the start time of all blocks by the specified duration.
        shift_end: Shift the end time of all blocks by the specified duration.
        fromJson: Load captions format from a JSON file.
        toJson: Save captions format to a JSON file.
        join: Joins another CaptionsFormat class data.
        joinFile: Joins CaptionsFormat data from file.
        __getitem__: Retrieve the block at the specified index.
        __setitem__: Set the block at the specified index.
        __str__: Return a string representation of the captions format.
        __iadd__: In-place addition for concatenating blocks.
        __isub__: In-place subtraction for removing blocks in a specific language.
        __iter__: Iterator for iterating through blocks.
        __len__: Return the number of blocks in the captions format.
        __enter__: Enter the context for managing resources.
        __exit__: Exit the context, handling exceptions.
    """

    extensions = FileExtensions()

    def __init__(self, filename: str = None, default_language: str = "und", length: str = None, **options):
        """
        Initialize a new instance of CaptionsFormat class.

        Parameters:
        - filename (str, optional): The name of the file associated with the captions, used for "with" keyword (default is None).
        - default_language (str, optional): The default language for captions (default is "und" for undefined).
        - **options: Additional keyword arguments for customization (e.g. metadata, style, ...).
        """
        self.time_length = 0
        self.filename = filename
        self.options = options or {}
        self._block_list: list[Block] = []
        self.setDefaultLanguage(default_language)

    def __getitem__(self, index: int):
        return self._block_list[index]

    def __setitem__(self, index: int, value: Block):
        self._block_list[index] = value

    def __iadd__(self, value):
        if not isinstance(value, CaptionsFormat):
            raise ValueError("Unsupported type. Must be an instance of `CaptionsFormat`")
        for i, value in enumerate(value):
            if i < len(self._block_list):
                self._block_list[i] += value
            else:
                self.append(value)
        return self

    def __isub__(self, language: str):
        for value in self._block_list:
            value -= language
        return self

    def __iter__(self):
        return iter(self._block_list)

    def __str__(self):
        return "\n".join(f"{i}. {caption}" for i, caption in enumerate(self._block_list))

    def __enter__(self):
        encoding = self.options.get("encoding") or "UTF-8"
        filename, ext = os.path.splitext(self.filename)
        if ext == ".json":
            self.fromJson(self.filename)
        else:
            with open(self.filename, "r", encoding=encoding) as stream:
                if self.detect(stream):
                    languages = self.getLanguagesFromFilename(self.filename)
                    self.setDefaultLanguage(languages[0])
                    self.read(stream, languages)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __len__(self):
        return len(self._block_list)

    def setDefaultLanguage(self, language: str):
        standardized = standardize_tag(language, macro=True)
        self.default_language = standardized if tag_is_valid(standardized) else "und"

    def insert(self, index: int, value: Block):
        self._block_list.insert(index, value)

    def detect(self, file: str | io.IOBase = None):
        raise ValueError("Not implemented")

    def read(self, content: str | io.IOBase, languages: list[str], **kwargs):
        raise ValueError("Not implemented")

    def checkContent(self, content: str | io.IOBase, languages: list[str] = None, **kwargs):
        if not isinstance(content, io.IOBase):
            if not not isinstance(content, str):
                raise ValueError("The content is not a unicode string or I/O stream.")
            content = io.StringIO(content)
        return content

    def save(self, filename: str, languages: list[str], **kwargs):
        raise ValueError("Not implemented")

    def makeFilename(self, filename: str, extension: str, languages: list[str] = None,
                     include_languages_in_filename: bool = True, **kwargs):
        languages = languages or [self.default_language]
        if filename.endswith(extension):
            file, _ = os.path.splitext(filename)
        else:
            file = filename
        if include_languages_in_filename:
            file = ".".join((val for val in file.split('.') if val not in languages))+"."+".".join(languages)

        return file+extension

    def getLanguagesFromFilename(self, filename):
        filename, ext = os.path.splitext(filename)
        filename = filename.split(".")
        if len(filename) > 1:
            languages = []
            for i in filename:
                try:
                    if tag_is_valid(standardize_tag(i, macro=True)):
                        languages.append(i)
                except Exception:
                    continue
            if not languages:
                languages = [self.default_language]
        else:
            languages = [self.default_language]
        return languages

    def append(self, item: Block):
        if item.end_time > self.time_length:
            self.time_length = item.end_time
        self._block_list.append(item)

    def shift_time(self, microseconds: int, miliseconds: int = 0, seconds: int = 0,
                   minutes: int = 0, hours: int = 0):
        microseconds += (miliseconds * 1_000 + seconds * 1_000_000 +
                         minutes * 60_000_000 + hours * 3_600_000_000)
        for i in self:
            i.shift_time_us(microseconds)

    def shift_start(self, microseconds: int, miliseconds: int = 0, seconds: int = 0,
                    minutes: int = 0, hours: int = 0):
        microseconds += (miliseconds * 1_000 + seconds * 1_000_000 +
                         minutes * 60_000_000 + hours * 3_600_000_000)
        for i in self:
            i.shift_start_us(microseconds)

    def shif_end(self, microseconds: int, miliseconds: int = 0, seconds: int = 0,
                 minutes: int = 0, hours: int = 0):
        microseconds += (miliseconds * 1_000 + seconds * 1_000_000 +
                         minutes * 60_000_000 + hours * 3_600_000_000)
        for i in self:
            i.shift_end_us(microseconds)

    def fromJson(self, file: str, **kwargs):
        encoding = kwargs.get("encoding") or "UTF-8"
        if not file.endswith(".json"):
            file += ".json"
        try:
            with open(file, "r", encoding=encoding) as f:
                data = json.load(f)
                self.time_length = data["time_length"]
                self.default_language = data["default_language"]
                self.filename = data["filename"]
                for key, value in data["extensions"].items():
                    setattr(FileExtensions, key, value)
                self.options = data["options"]
                self._block_list = [Block(**caption) for caption in data["block_list"]]
        except IOError as e:
            print(f"I/O error({e.errno}): {e.strerror}")
        except Exception as e:
            print(f"Error {e}")

    def toJson(self, file: str, **kwargs):
        encoding = kwargs.get("encoding") or "UTF-8"
        try:
            if not file.endswith(".json"):
                file += ".json"
            with open(file, "w", encoding=encoding) as f:
                json.dump({
                    "default_language": self.default_language,
                    "time_length": self.time_length,
                    "filename": self.filename,
                    "extensions": vars(self.extensions),
                    "options": self.options,
                    "block_list": self._block_list
                           }, f, default=vars)
        except IOError as e:
            print(f"I/O error({e.errno}): {e.strerror}")
        except Exception as e:
            print(f"Error {e}")

    def get_microseconds(self, microseconds: int, miliseconds: int = 0, seconds: int = 0,
                         minutes: int = 0, hours: int = 0):
        return (microseconds + miliseconds * 1_000 + seconds * 1_000_000 +
                minutes * 60_000_000 + hours * 3_600_000_000)

    def join(self, captionsFormat, add_end_time: bool = False, microseconds: int = 0, miliseconds: int = 0,
             seconds: int = 0, minutes: int = 0, hours: int = 0, **kwargs):
        """
        Join two CaptionsFormat instances by appending blocks from the provided format to the current format.

        Args:
            captionsFormat (CaptionsFormat): The CaptionsFormat instance to join with.
            add_end_time (bool, optional): If True, current end time is added to the time offset.
            microseconds (int, optional): Time offset by microseconds.
            miliseconds (int, optional): Time offset by milliseconds.
            seconds (int, optional): Time offset by seconds.
            minutes (int, optional): Time offset by minutes.
            hours (int, optional): Time offset by hours.
            **kwargs: Additional options for customization (e.g. file encoding).
        """
        if not isinstance(captionsFormat, CaptionsFormat):
            raise ValueError("Unsupported type. Must be an instance of `CaptionsFormat`")

        time_offset = self.get_microseconds(microseconds, miliseconds, seconds, minutes, hours)
        time_offset += self.time_length if add_end_time else 0

        for caption in captionsFormat:
            self.append(caption.copy())
            self[-1].shift_end_us(time_offset)

    def joinFile(self, filename: str, add_end_time: bool = False, microseconds: int = 0, miliseconds: int = 0,
                 seconds: int = 0, minutes: int = 0, hours: int = 0, **kwargs):
        """
        Join captions from file by appending blocks to the current format.

        Args:
            captionsFormat (CaptionsFormat): The CaptionsFormat instance to join with.
            add_end_time (bool, optional): If True, current end time is added to the time offset.
            microseconds (int, optional): Time offset by microseconds.
            miliseconds (int, optional): Time offset by milliseconds.
            seconds (int, optional): Time offset by seconds.
            minutes (int, optional): Time offset by minutes.
            hours (int, optional): Time offset by hours.
            **kwargs: Additional options for customization (e.g. file encoding).
        """
        encoding = kwargs.get("encoding") or "UTF-8"

        time_offset = self.get_microseconds(microseconds, miliseconds, seconds, minutes, hours)
        time_offset += self.time_length if add_end_time else 0

        with open(filename, "r", encoding=encoding) as stream:
            if self.detect(stream):
                self.read(stream, self.getLanguagesFromFilename(filename), time_offset=time_offset)
