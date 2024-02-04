import cssutils
from cssutils.css import CSSStyleSheet as originalCSSStyleSheet
from .styleFormat import cssParser
from .options import style_options


class StyleSheet(originalCSSStyleSheet):
    def __json__(self):
        return str(self.cssText)


cssutils.css.CSSStyleSheet = StyleSheet
