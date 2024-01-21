import json
import io
import os
from langcodes import standardize_tag, tag_is_valid
from .block import Block, BlockType
from .microTime import MicroTime as MT
import budoux



class FileExtensions:
    SAMI = ".sami"
    SRT = ".srt"
    SUB = ".sub"
    TTML = ".ttml"
    VTT = ".vtt"


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

    def __init__(self, file_name_or_content: str = None, default_language: str = "und",
                 time_length: MT = None, file_extensions = None,
                 media_height: int = None, media_width: int = None, isFile = True, **options):
        """
        Initialize a new instance of CaptionsFormat class.

        Parameters:
        - file_name_or_content (str, optional): The name of the file or file content/string associated with the captions, used for "with" keyword (default is None).
        - isFile (str, bool): Defines if file_name_or_content parameter is file name, used for "with" keyword (default is True).
        - default_language (str, optional): The default language for captions (default is "und" for undefined).
        - **options: Additional keyword arguments for customization (e.g. metadata, style, ...).
        """
        self.time_length = MT() or time_length
        self.file_name_or_content = file_name_or_content
        self.isFile = isFile
        self.media_height = media_height or 1080
        self.media_width = media_width or 1920
        self.options = options or {}
        if not self.options.get("blocks"):
            self.options["blocks"] = []
        if not self.options.get("layout"):
            self.options["layout"] = dict()
        if not self.options.get("style"):
            self.options["style"] = dict()
        if not self.options.get("metadata"):
            self.options["metadata"] = dict()
        if not self.options.get("style_metadata"):
            self.options["style_metadata"] = dict()
        if not self.options["style_metadata"].get("identifier_to_original"):
            self.options["style_metadata"]["identifier_to_original"] = dict()
        if not self.options["style_metadata"].get("identifier_to_new"):
            self.options["style_metadata"]["identifier_to_new"] = dict()
        if not self.options["style_metadata"].get("style_id_counter"):
            self.options["style_metadata"]["style_id_counter"] = 0
        self._block_list: list[Block] = []
        self.setDefaultLanguage(default_language)
        self.extensions = file_extensions or FileExtensions()

    def __getitem__(self, index: int):
        return self._block_list[index]

    def __setitem__(self, index: int, value: Block):
        self._block_list[index] = value

    def __delitem__(self, index: int):
        del self._block_list[index]

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
        if self.isFile:
            _, ext = os.path.splitext(self.file_name_or_content)
            if ext == ".json":
                self.fromJson(self.file_name_or_content)
            else:
                
                    with open(self.file_name_or_content, "r", encoding=encoding) as stream:
                        if self.detect(stream):
                            languages = self.getLanguagesFromFilename(self.file_name_or_content)
                            if languages and self.default_language == "und":
                                self.setDefaultLanguage(languages[0])
                            self.read(stream, languages)
        else:
            if self.detect(self.file_name_or_content):
                self.read(self.file_name_or_content)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __len__(self):
        return len(self._block_list)
    
    def getLines(self, lang: str = "und", lines: int = 0, split_block: bool = False, character_limit: int = 47, split_ratios: list[float] = [0.7, 1]) -> list[str]:
        """
        Format text of specific language into multiple lines.

        Args:
            lang (str, optional): Language code (default is "und" for undefined).
            lines (int, optional): The number of lines to format to. (default is 0 - autoformat). Ignores character limit and split ratios if it cannot fit in the desired amount.
            split_block (bool, optional): If the text cannot fit in desired lines (or 2 if autoformat), it will split the block (default is False).
            character_limit (int, optional) How many characters should be in a line. (default is 47)
            split_ratios (list[float], optional): Affects character_limit for n-th line. (default [0.7, 1])
        Returns:
            list[str]: A list of text lines.
            list[Block]: A list of extra blocks
        """
        text = self.get(lang)
        
        if lines == 1:
            return [text]

        if lang == "ja":
            parser = budoux.load_default_japanese_parser()
            phrases = parser.parse(text)
        elif lang in ["zh", "zh-CN", "zh-SG", "zh-Hans"]:
            parser = budoux.load_default_simplified_chinese_parser()
            phrases = parser.parse(text)
        elif lang in ["zh-HK", "zh-MO", "zh-TW", "zh-Hant"]:
            parser = budoux.load_default_simplified_chinese_parser()
            phrases = parser.parse(text)
        elif lang == "th":
            parser = budoux.load_default_thai_parser()
            phrases = parser.parse(text)
        else:
            phrases = text.split(" ")

        if lines != 0:
            total_characters = len(text)
            target_characters = total_characters - lines + 1
            current_limit = sum(character_limit * ratio for ratio in split_ratios)
            if current_limit < target_characters:
                remaining = (target_characters - current_limit) / total_characters
                for index, _ in enumerate(split_ratios):
                    split_ratios[index] += remaining  

        formatted_lines = []
        current_line = ""
        current_character_count = 0

        for phrase in phrases:
            current_ratio_index = min(len(formatted_lines), len(split_ratios) - 1)
            effective_limit = int(character_limit * split_ratios[current_ratio_index])
            print(effective_limit)

            if current_character_count + len(phrase) <= effective_limit:
                current_line += phrase + " "
                current_character_count += len(phrase) + 1  # +1 for the space
            else:
                formatted_lines.append(current_line.strip())
                current_line = phrase + " "
                current_character_count = len(phrase) + 1

        if current_line:
            formatted_lines.append(current_line.strip())

        return formatted_lines

     
    
    def setOptionsBlockId(self, index1, index2):
        block = self.options["blocks"][index1]
        if block.type == BlockType.LAYOUT:
            self.options["layout"][block.options["id"]] = index2
        elif block.type == BlockType.STYLE:
            self.options["style"][block.options["id"]] = index2
        elif block.type == BlockType.METADATA:
            self.options["metadata"][block.options["id"]] = index2
    
    def swapOptionsBlock(self, index1: int, index2: int):
        if index1 == index2 or index1 < 0 or index2 < 0:
            return
        self.setOptionsBlockId(index1, index2)
        self.setOptionsBlockId(index2, index1)
        self.options["blocks"][index1], self.options["blocks"][index2] = self.options["blocks"][index2], self.options["blocks"][index1]
    
    def deleteOptionsBlock(self, index: int):
        block = self.options["blocks"][index]
        if block.type == BlockType.LAYOUT:
            del self.options["layout"][block.options["id"]]
        elif block.type == BlockType.STYLE:
            del self.options["style"][block.options["id"]]
        elif block.type == BlockType.METADATA:
            del self.options["metadata"][block.options["id"]]
        del self.options["blocks"][index]
    
    def addLayout(self, id: str, layout: Block):
        if layout.block_type != BlockType.LAYOUT:
            raise ValueError(f"Expected BlockType {BlockType.METADATA} got {layout.block_type}")
        self.options["blocks"].append(layout)
        self.options["layout"][id] = len(self.options["blocks"])

    def getLayout(self, id: str):
        if id in self.options["layout"]:
            return self.options["blocks"][self.options["layout"][id]]
        return None
    
    def addStyle(self, id: str, style: Block):
        if style.block_type != BlockType.STYLE:
            raise ValueError(f"Expected BlockType {BlockType.METADATA} got {style.block_type}")
        self.options["blocks"].append(style)
        self.options["style"][id] = len(self.options["blocks"])
    
    def getStyle(self, id: str):
        if id in self.options["style"]:
            return self.options["blocks"][self.options["style"][id]]
        return None

    def addMetadata(self, id: str, metadata: Block):
        if metadata.block_type != BlockType.METADATA:
            raise ValueError(f"Expected BlockType {BlockType.METADATA} got {metadata.block_type}")
        self.options["blocks"].append(metadata)
        self.options["metadata"][id] = len(self.options["blocks"])
    
    def getMetadata(self, id: str):
        if id in self.options["metadata"]:
            return self.options["blocks"][self.options["metadata"][id]]
        return None

    def setDefaultLanguage(self, language: str):
        standardized = standardize_tag(language, macro=True)
        self.default_language = standardized if tag_is_valid(standardized) else "und"

    def insert(self, index: int, value: Block):
        self._block_list.insert(index, value)

    def detect(self, file: str | io.IOBase = None):
        raise ValueError("Not implemented")

    def read(self, content: str | io.IOBase, languages: list[str] = None, **kwargs):
        raise ValueError("Not implemented")

    def checkContent(self, content: str | io.IOBase, **kwargs):
        if not isinstance(content, io.IOBase):
            if not not isinstance(content, str):
                raise ValueError("The content is not a unicode string or I/O stream.")
            content = io.StringIO(content)
        return content

    def save(self, filename: str, languages: list[str] = None, **kwargs):
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
                return None
        else:
            return None
        return languages

    def append(self, item: Block):
        if item.end_time and item.end_time > self.time_length:
            self.time_length = item.end_time
        self._block_list.append(item)

    def shift_time(self, time: MT):
        for i in self:
            i.shift_time_us(time)

    def shift_start(self, time: MT):
        for i in self:
            i.shift_start_us(time)

    def shif_end(self, time: MT):
        for i in self:
            i.shift_end_us(time)

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

    def join(self, captionsFormat, add_end_time: bool = False, time: MT = None, **kwargs):
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

        time_offset = time or MT()
        if add_end_time:
            time_offset += self.time_length 

        for caption in captionsFormat:
            self.append(caption.copy())
            self[-1].shift_end_us(time_offset)

    def joinFile(self, filename: str, add_end_time: bool = False, time: MT = None, **kwargs):
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

        time_offset = time or MT()
        if add_end_time:
            time_offset += self.time_length 

        with open(filename, "r", encoding=encoding) as stream:
            if self.detect(stream):
                self.read(stream, self.getLanguagesFromFilename(filename), time_offset=time_offset)
