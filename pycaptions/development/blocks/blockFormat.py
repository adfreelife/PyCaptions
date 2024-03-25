import copy

from collections import defaultdict
from langcodes import standardize_tag, tag_is_valid
from ...microTime import MicroTime as MT
from ...styling import Styling
from ..textFormat import get_phrases, get_lines_ratio
from ..css import cssParser


class BlockFormat:
    """
    Represents a block of content in a multimedia file or document.

    Methods:
        copy: Returns a copy of the current block.
    """
    def __init__(self, block_type: int, value = None, **options):
        self.block_type = block_type
        self.value = value

        if "start_time" in options:
            self.start_time = options.pop("start_time")
            self.end_time = options.pop("end_time")

        if "options" in options:
            self.options = options["options"]
        else:
            self.options = options or {}

    def copy(self):
        return copy.deepcopy(self)

    