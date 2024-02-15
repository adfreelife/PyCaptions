import cssutils

from cssutils import CSSParser
from cssutils.css import CSSStyleSheet as originalCSSStyleSheet


class StyleSheet(originalCSSStyleSheet):
    def __json__(self):
        return str(self.cssText)


cssutils.css.CSSStyleSheet = StyleSheet

cssParser = CSSParser(validate=False)
