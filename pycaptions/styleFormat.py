import webcolors
import colorsys
import re

from bs4 import BeautifulSoup as BS
from cssutils import CSSParser


cssParser = CSSParser(validate=False)


def to_hex2(value):
    return '{:02X}'.format(value)


def get_hexrgb(color):
    if color.startswith("#"):
        if len(color) == 5:
            color = color[:-1]
        if len(color) == 9:
            color = color[:-2]
        return [to_hex2(i) for i in webcolors.hex_to_rgb(color)]
    elif color.endswith(")"):
        if color.startswith("rgb"):
            return [to_hex2(int(i)) for i in color[4:-1].split(",")]
        colors = [re.sub(r'[^0-9.]', '', i)  for i in color[:-1].split("(")[1].split(",")]
        if color.startswith("hsl"):
            h = float(colors[0]) 
            s = float(colors[1])
            l = float(colors[2])
            if h > 1:
                h /= 360
            if s > 1:
                s /= 100
            if l > 1:
                l /= 100
            return [to_hex2(min(int(i*255),255)) for i in colorsys.hls_to_rgb(h,l,s)]
        print(f"No color parser for {color}")
        return ["00","00","00"]
    else:
        return [to_hex2(i) for i in webcolors.name_to_rgb(color)]


class StyleFormat(BS):

    def parseStyle(self, string):
        return cssParser.parseStyle(string, encoding="UTF-8")
    
    def get_lines(self):
        return (BS(line, 'html.parser').get_text() for index, line in enumerate(str(self).split("<br/>")))
