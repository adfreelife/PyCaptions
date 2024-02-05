import cssutils

from bs4 import BeautifulSoup as BS
from cssutils import CSSParser
from cssutils.css import CSSStyleSheet as originalCSSStyleSheet


class StyleSheet(originalCSSStyleSheet):
    def __json__(self):
        return str(self.cssText)


cssutils.css.CSSStyleSheet = StyleSheet

cssParser = CSSParser(validate=False)


class StyleFormat(BS):

    def parseStyle(self, string):
        return cssParser.parseStyle(string, encoding="UTF-8")
    
    def get_lines(self):
        return (BS(line, 'html.parser').get_text() for index, line in enumerate(str(self).split("<br/>")))
