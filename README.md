# PyCaptions

PyCaptions is a caption reading/writing library.

* * *
- [Installation](#installation)
- [Supported Formats](#supported-formats)
- [Examples](#examples)
* * *

## Installation
- PIP
    ```
    pip install --upgrade pycaptions
    ```
- Source
    ```
    git clone https://github.com/adfreelife/PyCaptions.git
    cd PyCaptions
    python setup.py install
    ```

## Supported Formats
- [Synchronized Accessible Media Interchange (SAMI)](https://learn.microsoft.com/en-us/previous-versions/windows/desktop/dnacc/understanding-sami-1.0)
- [SubRip (SRT)](https://en.wikipedia.org/wiki/SubRip)
- [MicroDVD (SUB)](https://en.wikipedia.org/wiki/MicroDVD)
- [Timed Text Markup Language (TTML, DFXP, ...)](https://www.w3.org/TR/ttml/)
- [Web Video Text Tracks Format (VTT)](https://www.w3.org/TR/webvtt/)

## Examples

### Generic from file name
```python
from pycaptions import Captions

with Captions("tests/test.en.srt") as captions:
    captions.saveVTT("test")
```

### Generic from file stream
```python
with open("tests/test.en.srt", encoding="UTF-8") as f:
    captions = Captions(f) # or captions = Captions()
                           # captions.read(f)
    captions.saveVTT("test")
```

### Generic from string
```python
srt = """1
00:00:00,500 --> 00:00:02,000
This is a test file
"""
captions = Captions(srt) # or captions = Captions()
                         # captions.detect(srt)
captions.saveVTT("test")
```

### Specific
Have the same functions as generic, except

```python
from pycaptions import SubRip, detectSRT

with open("tests/test.en.srt", encoding="UTF-8") as f:
    if detectSRT(f): # or SubRip.detect(f)
        captions = SubRip().read(f)
        captions.saveVTT("test")
```

### Multilangual
```python
from pycaptions import Captions

with Captions("tests/test.en.srt") as captions:
    with Captions("tests/test.es.srt") as captions2:
        captions+=captions2
    # first line will be in english, second one in spanish
    captions.save("test", ["en","es"]) 
```
