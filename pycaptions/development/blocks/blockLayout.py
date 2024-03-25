from .blockFormat import BlockFormat
from ..blockType import BlockType

class LayoutBlock(BlockFormat):
    def __init__(self, value=None, **options):
        super().__init__(BlockType.LAYOUT, value, **options)