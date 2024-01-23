from bs4 import BeautifulSoup as BS
from cssutils import CSSParser
from cssutils.css import CSSStyleSheet as originalCSSStyleSheet
import cssutils


class StyleSheet(originalCSSStyleSheet):
    def __json__(self):
        return str(self.cssText)


cssutils.css.CSSStyleSheet = StyleSheet
cssParser = CSSParser(validate=False)


class Styling(BS):

    def parseStyle(self, string):
        return cssParser.parseStyle(string, encoding="UTF-8")

    @staticmethod
    def fromSRT(text):
        bs = BS(text, "html.parser")
        if bs.font:
            for tag in bs.find_all("font"):
                tag.name = "p"
                if "color" in tag.attrs:
                    tag["style"] = f'color: {tag["color"]};'
                    del tag["color"]
                if "size" in tag.attrs:
                    tag["style"] = tag.get("style", "")+f'font-size: {tag["size"]}pt;'
                    del tag["size"]
                if "face" in tag.attrs:
                    tag["style"] = tag.get("style", "")+f'font-family: {tag["face"]};'
                    del tag["face"]
        return str(bs)
    
    def getSRT(self, css = None, add_metadata = True):
        for tag in self.find_all():
            if tag.name:
                if tag.get("style"):
                    css = self.parseStyle(tag.get("style"))
                    font_tag = self.new_tag("font")
                    wrap_in_font = False
                    for prop in css:
                        prop_name = prop.name.lower()
                        prop_value = str(prop.value)
                        if prop_name == "color":
                            font_tag["color"] = prop_value
                            wrap_in_font = True
                        elif prop_name == "font-size":
                            font_tag["size"] = prop_value
                            wrap_in_font = True
                        elif prop_name == "font-family":
                            font_tag["face"] = prop_value
                            wrap_in_font = True
                        elif prop_name == "font-weight" and prop_value == "bold":
                            tag.string.wrap(self.new_tag("b"))
                        elif prop_name == "font-style" and prop_value == "italic":
                            tag.string.wrap(self.new_tag("i"))
                        elif prop_name == "text-decoration" and prop_value == "underline":
                            tag.string.wrap(self.new_tag("u"))
                    if wrap_in_font:
                        tag.string.wrap(font_tag)
                elif tag.get("id"):
                    pass
                elif tag.get("class"):
                    pass
                tagname = tag.name.split(".")
                if len(tagname) == 2:
                    if add_metadata:
                        tag.insert_before("["+tagname[1]+"] ")
                    tag.string.wrap(self.new_tag(tagname[0]))
                tagname = tagname[0]

                if tag.name == ["b", "u", "i"]:
                    tag.string.wrap(self.new_tag(tag.name))
                    tag.unwrap()
                elif tag.name == "font":
                    font_tag = self.new_tag(tag.name)
                    if tag.get("color"):
                        font_tag["color"] = tag.get("color")
                    if tag.get("size"):
                        font_tag["size"] = tag.get("size")
                    if tag.get("face"):
                        font_tag["face"] = tag.get("face")
                    tag.string.wrap(font_tag)
                    tag.unwrap()
                else:
                    tag.unwrap()

        return str(self)

    def getTTML(self, css = None, add_metadata = True):
        return self.get_text()    
