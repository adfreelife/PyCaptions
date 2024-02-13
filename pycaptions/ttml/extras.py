# this structure is subject to change
TTML_PROPERTIES = {
    "tts:backgroundClip": {
        "css": "background-clip",
        "values": ["border", "content", "padding"],
        "tags": ["body", "div", "image", "p", "region", "span"]
    },
    "tts:backgrounColor": {
        "css": "background-color",
        "values-map": {
            "fuchsia": "magenta",
            "aqua": "cyan"
        },
        "values": ["<color>"],
        "tags": ["body", "div", "image", "p", "region", "span"]
    },
    "tts:backgroundExtent": {
        "css": "background-size",
        "values": ["<extent>"],
        "tags": ["body", "div", "image", "p", "region", "span"]
    },
    "tts:backgroundImage": {
        "css": "background-image",
        "values": ["none", "<image>"],
        "tags": ["body", "div", "image", "p", "region", "span"]
    },
    "tts:backgroundOrigin": {
        "css": "background-origin",
        "values": ["border", "content", "padding"],
        "tags": ["body", "div", "image", "p", "region", "span"]
    },
    "tts:backgroundPosition": {
        "css": "background-position",
        "values": ["<position>"],
        "tags": ["body", "div", "image", "p", "region", "span"]
    },
    "tts:backgroundRepeat": {
        "css": "background-repeat",
        "values-map": {
            "repeatX": "repeat-x",
            "repeatY": "repeat-y",
            "noRepeat": "no-repeat"
        },
        "values": ["repeat", "repeatX", "repeatY", "noRepeat"],
        "tags": ["body", "div", "image", "p", "region", "span"]
    },
    "tts:border": {
        "css": "border",
        "values": ["<border>"],
        "tags": ["body", "div", "image", "p", "region", "span"]
    },
    "tts:bpd": {
        "css": None,
        "values": ["<measures>"],
        "tags": ["body", "div", "p", "span"]
    },
    "tts:color": {
        "css": "color",
        "values-map": {
            "fuchsia": "magenta",
            "aqua": "cyan"
        },
        "values": ["<color>"],
        "tags": ["span"]
    },
    "tts:direction": {
        "css": "direction",
        "values": ["ltr", "rtl"],
        "tags": ["p", "span"]
    },
    "tts:disparity": {
        "css": None,
        "values": ["<length>"],
        "tags": ["div", "p", "region"]
    },
    "tts:display": {
        "css": "display",
        "values-map": {
            "inlineBlock": "inline-block"
        },
        "values": ["auto", "none", "inlineBlock"],
        "tags": ["body", "div", "image", "p", "region", "span"]
    },
    "tts:displayAlign": {
        "css": "display-align",
        "values-map": {
            "before": "flex-start",
            "after": "flex-end",
            "justify": "space-between"
        },
        "values": ["before", "center", "after", "justify"],
        "tags": ["body", "div", "p", "region"]
    },
    "tts:extent": {
        "css": None,
        "values": ["<extent>"],
        "tags": ["tt", "div", "image", "p", "region"]
    },
    "tts:fontFamily": {
        "css": "font-family",
        "values": ["<font-families>"],
        "tags": ["span"]
    },
    "tts:fontKerning": {
        "css": "font-kerning",
        "values": ["none", "normal"],
        "tags": ["span"]
    },
    "tts:fontSelectionStrategy": {
        "css": None,
        "values": ["auto", "character"],
        "tags": ["span"]
    },
    "tts:fontShear": {
        "css": None, #skewX skewY
        "values": ["<percentage>"],
        "tags": ["span"]
    },
    "tts:fontSize": {
        "css": "font-size",
        "values": ["<font-size>"],
        "tags": ["span"]
    },
    "tts:fontStyle": {
        "css": "font-style",
        "values": ["normal", "italic", "oblique"],
        "tags": ["span"]
    },
    "tts:fontVariant": {
        "css": None,
        "values": ["<font-variant>"],
        #font-variant-east-asian: Only full-width, rubyfont-variant-position: normal, sub, superfont-feature-settings: Only hwid
        "tags": ["span"]
    },
    "tts:fontWeight": {
        "css": "font-weight",
        "values": ["normal", "bold"],
        "tags": ["span"]
    },
    "tts:ipd": {
        "css": None,
        "values": ["<measure>"],
        "tags": ["body", "div", "p", "span"]
    },
    "tts:letterSpacing": {
        "css": "letter-spacing",
        "values": ["normal", "<length>"],
        "tags": ["span"]
    },
    "tts:lineHeight": {
        "css": "line-height",
        "values": ["normal", "<length>"],
        "tags": ["p"]
    },
    "tts:lineShear": {
        "css": None, #skewX skewY
        "values": ["<percentage>"],
        "tags": ["p"]
    },
    "tts:luminanceGain": {
        "css": None,
        "values": ["<non-negative-number>"],
        "tags": ["region"]
    },
    "tts:opacity": {
        "css": "opacity",
        "values": ["<alpha>"],
        "tags": ["body", "div", "image", "p", "region", "span"]
    },
    "tts:origin": {
        "css": None,
        "values": ["<origin>"],
        "tags": ["div", "p", "region"]
    },
    "tts:overflow": {
        "css": "overflow",
        "values": ["visible", "hidden"],
        "tags": ["region"]
    },
    "tts:padding": {
        "css": "padding",
        "values": ["<padding>"],
        "tags": ["body", "div", "image", "p", "region", "span"]
    },
    "tts:position": {
        "css": "background-position",
        "values": ["<position>"],
        "tags": ["body", "div", "image", "p", "region", "span"]
    },
    "tts:ruby": {
        "css": "ruby",
        "values": ["none", "container", "base", "baseContainer", "text", "textContainer", "delimiter"],
        "tags": ["span"]
    },
    "tts:rubyAlign": {
        "css": "ruby-align",
        "values": ["start", "center", "end", "spaceAround", "spaceBetween", "withBase"],
        "tags": ["span"]
    },
    "tts:rubyPosition": {
        "css": None,
        "values": ["before", "after", "outside"],
        "tags": ["span"]
    },
    "tts:rubyReserve": {
        "css": None,
        "values": ["<ruby-reserve>"],
        "tags": ["p"]
    },
    "tts:shear": {
        "css": None, #skewX skewY
        "values": ["<percentage>"],
        "tags": ["p"]
    },
    "tts:showBackground": {
        "css": None,
        "values": ["always", "whenActive"],
        "tags": ["region"]
    },
    "tts:textAlign": {
        "css": "text-align",
        "values": ["left", "center", "right", "start", "end", "justify"],
        "tags": ["p"]
    },
    "tts:textCombine": {
        "css": "text-combine-upright",
        "values": ["<text-combine>"],
        "tags": ["span"]
    },
    "tts:textDecoration": {
        "css": "text-decoration",
        "values-map": {
            "line-through": "lineThrough",
            "noUnderline": None,
            "noLineThrough": None,
            "noOverline": None
        },
        "values": ["<text-decoration>"],
        "tags": ["span"]
    },
    "tts:textEmphasis": {
        "css": "text-emphasis-position",
        #emphasis-style maps to text-emphasis-style; emphasis-color maps to text-emphasis-color; emphasis-position maps to text-emphasis-position
        "values": ["<text-emphasis>"],
        "tags": ["span"]
    },
    "tts:textOrientation": {
        "css": "text-orientation",
        "values": ["mixed", "sideways", "upright"],
        "tags": ["span"]
    },
    "tts:textOutline": {
        "css": None,
        "values": ["<text-outline>"],
        "tags": ["span"]
    },
    "tts:textShadow": {
        "css": "text-shadow",
        "values": ["<text-shadow>"],
        "tags": ["span"]
    },
    "tts:unicodeBidi": {
        "css": "unicode-bidi",
        "values-map": {
            "isolate": None
        },
        "values": ["normal", "embed", "bidiOverride", "isolate"],
        "tags": ["p", "span"]
    },
    "tts:visibility": {
        "css": "visibility",
        "values": ["visible", "hidden"],
        "tags": ["body", "div", "image", "p", "region", "span"]
    },
    "tts:wrapOption": {
        "css": None,
        "values": ["wrap", "noWrap"],
        "tags": ["span"]
    },
    "tts:writingMode": {
        "css": None,
        "values": ["lrtb", "rltb", "tbrl", "tblr", "lr", "rl", "tb"],
        "tags": ["region"]
    },
    "tts:zIndex": {
        "css": "z-index",
        "values": ["auto", "<integer>"],
        "tags": ["region"]
    }
}

TTML_FROM_CSS = {
    "background-clip": "tts:backgroundClip",
    "background-color": "tts:backgrounColor",
    "background-size": "tts:backgroundExtent",
    "background-image": "tts:backgroundImage",
    "background-origin": "tts:backgroundOrigin",
    "background-position": "tts:position",
    "background-repeat": "tts:backgroundRepeat",
    "border": "tts:border",
    "color": "tts:color",
    "direction": "tts:direction",
    "display": "tts:display",
    "display-align": "tts:displayAlign",
    "font-family": "tts:fontFamily",
    "font-kerning": "tts:fontKerning",
    "font-size": "tts:fontSize",
    "font-style": "tts:fontStyle",
    "font-weight": "tts:fontWeight",
    "letter-spacing": "tts:letterSpacing",
    "line-height": "tts:lineHeight",
    "opacity": "tts:opacity",
    "overflow": "tts:overflow",
    "padding": "tts:padding",
    "ruby": "tts:ruby",
    "ruby-align": "tts:rubyAlign",
    "text-align": "tts:textAlign",
    "text-combine-upright": "tts:textCombine",
    "text-decoration": "tts:textDecoration",
    "text-emphasis-position": "tts:textEmphasis",
    "text-orientation": "tts:textOrientation",
    "text-shadow": "tts:textShadow",
    "unicode-bidi": "tts:unicodeBidi",
    "visibility": "tts:visibility",
    "z-index": "tts:zIndex"
}

def tryparse(func):
    def wrapper(value):
        try:
            return func(value=value)
        except:
            return False
    return wrapper

@tryparse
def checkAlpha(value):
    if not value or value == "NaN" or value == "none":
        return 0
    else:
        return max(min(1, float(value)), 0)
    
def checkBorder(value):
    #<border-thickness> || <border-style> || <border-color> || <border-radii>
    pass

def checkColor(value):
    """
    : "#" rrggbb
  | "#" rrggbbaa
  | "rgb(" r-value "," g-value "," b-value ")"
  | "rgba(" r-value "," g-value "," b-value "," a-value ")"
  | <named-color>
    """

def checkExtent(value):
    """
    : "auto"
  | "contain"
  | "cover"
  | <measure> <lwsp> <measure>
    """

def checkFontFamilies(value):
    """
    <font-families>
  : font-family (<lwsp>? "," <lwsp>? font-family)*

font-family
  : <family-name>
  | <generic-family-name>
    """

def checkFontSize(value):
    """
    <font-size>
  : <length> (<lwsp> <length>)?
    """

def checkFontVariant(value):
    """
    <font-variant>
  : "normal"
  | ("super" | "sub") || ("full" | "half") || "ruby"
    """

def checkImage(value):
    """
    <image>
  : <uri>
    """

@tryparse
def checkInteger(value):
    return str(int(value)) == value

def checkLength(value):
    """
    <length>
  : scalar
  | <percentage>

scalar
  : <number> units

units
  : "px"
  | "em"
  | "c"                                     // abbreviation of "cell"
  | "rw"
  | "rh"
    """

def checkMeasure(value):
    """
    : "auto"
  | "fitContent"
  | "maxContent"
  | "minContent"
  | <length>
    """

@tryparse
def checkPositiveInteger(value):
    return int(value) > 0

def checkOrigin(value):
    """
    <origin>
  : "auto"
  | <length> <lwsp> <length>
    """

def checkPadding(value):
    """
    <padding>
  : <length> <lwsp> <length> <lwsp> <length> <lwsp> <length>
  | <length> <lwsp> <length> <lwsp> <length>
  | <length> <lwsp> <length>
  | <length>
    """

def checkPercentage(value):
    """
    <percentage>
  : <number> "%"
    """

def checkPosition(value):
    """
    <position>
  : offset-position-h                             // single component value
  | edge-keyword-v                                // single component value
  | offset-position-h <lwsp> offset-position-v    // two component value
  | position-keyword-v <lwsp> position-keyword-h  // two component value
  | position-keyword-h <lwsp> edge-offset-v       // three component value
  | position-keyword-v <lwsp> edge-offset-h       // three component value
  | edge-offset-h <lwsp> position-keyword-v       // three component value
  | edge-offset-v <lwsp> position-keyword-h       // three component value
  | edge-offset-h <lwsp> edge-offset-v            // four component value
  | edge-offset-v <lwsp> edge-offset-h            // four component value

offset-position-h
  : position-keyword-h
  | <length>

offset-position-v
  : position-keyword-v
  | <length>

edge-offset-h
  : edge-keyword-h <lwsp> <length>

edge-offset-v
  : edge-keyword-v <lwsp> <length>

position-keyword-h
  : "center"
  | edge-keyword-h

position-keyword-v
  : "center"
  | edge-keyword-v

edge-keyword-h
  : "left"
  | "right"

edge-keyword-v
  : "top"
  | "bottom"
    """

def checkRubyReserve(value):
    """
    <ruby-reserve>
  : "none"
  | ("both" | <annotation-position>) (<lwsp> <length>)?
    """

def checkTextCombine(value):
    """
    <text-combine>
  : "none"
  | "all"
    """

def checkTextDecoration(value):
    """
    <text-decoration>
  : "none"
  | (("underline" | "noUnderline") || ("lineThrough" | "noLineThrough") || ("overline" | "noOverline"))
    """

def checkTextEmphasis():
    """
    <text-emphasis>
  : <emphasis-style> || <emphasis-color> || <emphasis-position>
    """

def checkTextOutline(value):
    """
    <text-outline>
  : "none"
  | (<color> <lwsp>)? <length> (<lwsp> <length>)?
    """

def checkTextShadow(value):
    """
    <text-shadow>
  : "none"
  | <shadow> (<lwsp>? "," <lwsp>? <shadow>)*
    """


TTML_VALUE_GROUPS = {
    "<alpha>": checkAlpha,
    "<border>": checkBorder,
    "<color>": checkColor,
    "<extent>": checkExtent,
    "<font-families>": checkFontFamilies,
    "<font-size>": checkFontSize,
    "<font-variant>": checkFontVariant,
    "<image>": checkImage,
    "<integer>": checkInteger,
    "<length>": checkLength,
    "<measures>": checkMeasure,
    "<non-negative-number>": checkPositiveInteger,
    "<origin>": checkOrigin,
    "<padding>": checkPadding,
    "<percentage>": checkPercentage,
    "<position>": checkPosition,
    "<ruby-reserve>": checkRubyReserve,
    "<text-combine>": checkTextCombine,
    "<text-decoration>": checkTextDecoration,
    "<text-emphasis>": checkTextEmphasis,
    "<text-outline>": checkTextOutline,
    "<text-shadow>": checkTextShadow,
}