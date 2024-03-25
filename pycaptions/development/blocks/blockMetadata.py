from .blockFormat import BlockFormat
from ..blockType import BlockType


class MetadataBlock(BlockFormat):
    def __init__(self, value=None, **options):
        super().__init__(BlockType.METADATA, value, **options)