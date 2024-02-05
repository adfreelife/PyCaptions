from ..development.colors import get_hexrgb
from bs4 import BeautifulSoup as BS


@staticmethod
def fromSRT(text):
    bs = BS(text, "html.parser")
    if bs.font:
        for tag in bs.find_all("font"):
            tag.name = "span"
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

def getSRT(self, lines:int = -1, options: dict =  None, 
            add_metadata: bool = True, **kwargs):
    for tag in self.find_all():
        if tag.name:
            if tag.get("style"):
                inline_css = self.parseStyle(tag.get("style"))
                font_tag = self.new_tag("font")
                wrap_in_font = False
                for prop in inline_css:
                    prop_name = prop.name.lower()
                    prop_value = str(prop.value)
                    if prop_name == "color":
                        font_tag["color"] = "#"+"".join(get_hexrgb(prop_value))
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
            if tag.get("class"):
                pass
            tagname = tag.name.split(".")
            if len(tagname) == 2:
                if add_metadata:
                    tag.insert_before("["+tagname[1]+"] ")
                tag.string.wrap(self.new_tag(tagname[0]))
            tagname = tagname[0]

            if tag.name in ["b", "u", "i"]:
                tag.string.wrap(self.new_tag(tag.name))
                tag.unwrap()
            elif tag.name == "font":
                font_tag = self.new_tag(tag.name)
                if tag.get("color"):
                    font_tag["color"] = "#"+"".join(get_hexrgb(tag.get("color")))
                if tag.get("size"):
                    font_tag["size"] = tag.get("size")
                if tag.get("face"):
                    font_tag["face"] = tag.get("face")
                tag.string.wrap(font_tag)
                tag.unwrap()
            elif tag.name == "br":
                if lines == 1:
                    tag.insert_before(" ")
                else:
                    tag.insert_before("\n")
                tag.unwrap()
            else:
                tag.unwrap()

    return str(self)