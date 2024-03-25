
from collections import defaultdict
from langcodes import standardize_tag, tag_is_valid
from ...microTime import MicroTime as MT
from ...styling import Styling
from ..textFormat import get_phrases, get_lines_ratio
from .blockFormat import BlockFormat
from ..blockType import BlockType


class CaptionBlock(BlockFormat):
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
    def __init__(self, value: Styling = None, language: str = "und", start_time: MT = None,
                 end_time: MT = None, **options):
        """
        Initialize a new instance of the Block class.

        Parameters:
        - language (str, optional): The language of the text in the block (default is "und" for undefined).
        - start_time (int, optional): The starting time of the block in microseconds (default is 0).
        - end_time (int, optional): The ending time of the block in microseconds (default is 0).
        - **options: Additional keyword arguments for customization (e.g style, layout, ...).
        """
        super().__init__(BlockType.CAPTION, None, start_time=start_time, end_time=end_time, **options)
        self.value = defaultdict(str)
        if value:
            if isinstance(value, dict):
                for i, j in value.items():
                    self[i] = j
            else:
                self.value[language] = value
        
    def __getitem__(self, index: str):
        return self.value[index]
    
    def __setitem__(self, index: str, value):
        self.value[index] = Styling(value, "html.parser")

    def __delitem__(self, index: str):
        del self.value[index]

    def __str__(self):
        temp = '\n'.join(f" {lang}: {text}" for lang, text in self.value.items())
        return f"start: {self.start_time} end: {self.end_time}\n{temp}"

    def __iadd__(self, value):
        if not isinstance(value, CaptionBlock):
            raise ValueError("Unsupported type. Must be an instance of `Block`")
        for key, language in value:
            self.value[key] = language
        return self

    def __add__(self, value):
        if not isinstance(value, CaptionBlock):
            raise ValueError("Unsupported type. Must be an instance of `Block`")
        out = self.copy()
        for key, language, comment in value:
            out.value[key] = language
        return out

    def __isub__(self, language: str):
        if language in self.value:
            del self.value[language]
        return self

    def __sub__(self, language: str):
        out = self.copy()
        if language in out.value:
            del out.value[language]
        return out

    def __iter__(self):
        self._keys_iterator = iter(self.value)
        return self

    def __next__(self):
        try:
            key = next(self._keys_iterator)
            return key, self.value.get(key)
        except StopIteration:
            raise StopIteration

    def get(self, lang: str, lines: int = -1, **kwargs) -> str:
        return self.get_lines(lang, lines, **kwargs)

    def get_style(self, lang: str) -> str:
        return self.value.get(lang)
    
    def _language_lines(self, lang):
        return self.value.get(lang).get_lines()

    def get_lines(self, lang: str = None, lines: int = 0, character_limit: int = 47,
                  split_ratios: list[float] = [0.7, 1], smaller_first_line: bool = True, **kwargs) -> list[str]:
        """
        Format text of specific language into multiple lines.

        Args:
            lang (str, optional): Language code (default is None - uses default_language).
            lines (int, optional): The number of lines to format to. (default is 0 - autoformat). Ignores character limit and split ratios if it cannot fit in the desired amount.
            character_limit (int, optional) How many characters should be in a line. (default is 47)
            split_ratios (list[float], optional): Affects character_limit for n-th line. (default [0.7, 1])
            parser_language (str, optional): Parser language code, if None it uses lang.
        Returns:
            list[str]: A list of text lines.
        """

        lang = lang or next(iter(self.value))

        if lines == -1:
            return self._language_lines(lang)

        separator = " "
        if "separator" in kwargs:
            separator = kwargs["separator"]

        text_lines = self._language_lines(lang)
        text = next(text_lines)
        if text.endswith("-"):
            add_separator = False
        else:
            add_separator = True

        for i in text_lines:
            if add_separator:
                text += separator
            if i.endswith("-"):
                text += i[::-1]
                add_separator = False
            else:
                text += i
                add_separator = True

        length = len(text)

        if lines == 1:
            return [text]

        standardized = standardize_tag(kwargs.get("parser_language") or lang, macro=True)
        standardized = standardized if tag_is_valid(standardized) else "und"
        
        phrases = get_phrases(text, standardized)

        split_ratios = get_lines_ratio(lines, length, character_limit, split_ratios, smaller_first_line)

        formatted_lines = []
        current_line = []
        current_character_count = 0

        for index, phrase in enumerate(phrases):
            current_ratio_index = min(len(formatted_lines), len(split_ratios) - 1)
            effective_limit = int(character_limit * split_ratios[current_ratio_index])

            if current_character_count + len(phrase) <= effective_limit:
                current_line.append(phrase)
                current_character_count += len(phrase) + 1  # +1 for the space
            elif index+1 == len(phrases):
                current_line.append(phrase)
            else:
                formatted_lines.append(separator.join(current_line))
                current_line= [phrase]
                current_character_count = len(phrase) + 1

        if current_line:
            formatted_lines.append(separator.join(current_line))

        return formatted_lines

    def append(self, text: Styling, lang: str = None, separator: str = "<br>"):
        lang = lang or next(iter(self.value))
        if self.value[lang]:
            self.value[lang].append(separator)
            self.value[lang].append(text)
        else:
            self.value[lang] = text

    def append_without_common_part(self, text: str, lang: str = None):
        lang = lang or next(iter(self.value))
        common_lenght = 0
        current = self.get(lang).get_lines()
        min_length = min(len(current), len(text))

        for i in range(min_length):
            if current[-i:] == text[:i]:
                common_lenght = i

        self[lang] = current + text[common_lenght:]

    def shift_time_us(self, microseconds: int):
        self.start_time += microseconds
        self.end_time += microseconds

    def shift_time(self, time: MT):
        self.start_time += time
        self.end_time += time

    def shift_start_us(self, microseconds: int):
        self.start_time += microseconds

    def shift_start(self, time: MT):
        self.start_time += time

    def shift_end_us(self, microseconds: int):
        self.end_time += microseconds

    def shift_end(self, time: MT):
        self.end_time += time