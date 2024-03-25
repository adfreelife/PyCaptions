from .blockFormat import BlockFormat
from ..css import cssParser
from ..blockType import BlockType


class StyleBlock(BlockFormat):
    def __init__(self, value=None, **options):
        super().__init__(BlockType.STYLE, value, **options)
        self.options["style"] = cssParser.parseString(cssText=self.options["style"], encoding="UTF-8")
        