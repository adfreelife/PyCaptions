from .blockFormat import BlockFormat
from ...styling import Styling
from ..blockType import BlockType

class CommentBlock(BlockFormat):

    def __init__(self, value=None, **options):
        super().__init__(BlockType.COMMENT, value, **options)

    def __setitem__(self, index: str, value):
        self.value = value

    def append(self, text: Styling, separator: str = "\n", **other):
        if self.value:
            self.value+=separator+text
        else:
            self.value = text