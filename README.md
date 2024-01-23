<h1 align="center">PyCaptions</h1>
<p align="center">
  <a href="https://pypi.org/project/pycaptions"><img alt="PyPI - Version" src="https://img.shields.io/pypi/v/pycaptions.svg?color=blue"></a>
  <a href="https://pypi.org/project/pycaptions"><img alt="PyPI - License" src="https://img.shields.io/pypi/l/pycaptions.svg"></a>
  <a href="https://pypi.org/project/pycaptions"><img alt="PyPI - Python" src="https://img.shields.io/pypi/pyversions/pycaptions.svg?color=blue"></a>
  <a href="https://pypi.org/project/pycaptions"><img alt="PyPI - Wheel" src="https://img.shields.io/pypi/wheel/pycaptions.svg"></a>
  <a href="https://pypi.org/project/pycaptions"><img alt="PyPI - Status" src="https://img.shields.io/pypi/status/pycaptions.svg"></a>
  <a href="https://pypi.org/project/pycaptions"><img alt="PyPI - Downloads" src="https://static.pepy.tech/personalized-badge/pycaptions?period=total&units=international_system&left_text=downloads&left_color=grey&right_color=blue"></a>
</p>
PyCaptions is a caption reading/writing library.

* * *

**Why [LGPL-3.0](https://choosealicense.com/licenses/lgpl-3.0/)?** This is just to ensure that source code for the library is always under the same licence and cannot be closed-sourced. All the conditions for this licence only apply for the the library itself and it's modifications. We reccomend to just contribute to the project if you are making modifications, unless they are drastic and specific to your case.

* * *
Table of Contents
- [Installation](#installation)
- [Supported Formats](#supported-formats)
- [Plans](#future-plans)
- [Examples](#examples)
- [Changelog](#changelog)
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
- [SubRip (SRT)](https://en.wikipedia.org/wiki/SubRip) (reader + writer)
- [MicroDVD (SUB)](https://en.wikipedia.org/wiki/MicroDVD) (reader + writer*)
- [Timed Text Markup Language (TTML, DFXP, XML)](https://www.w3.org/TR/ttml/) (reader* + writer*)
- [Web Video Text Tracks Format (VTT)](https://www.w3.org/TR/webvtt/) (reader + writer*)

*reader\* - does not read styling/layout/metadata*
<br>*writer\* - does not write styling layout/metadata*

## Future plans
- add writers to all supported formats
- auto-fit lines into multilines or split captions blocks into two parts
- add support for more formats
    - [Synchronized Accessible Media Interchange (SAMI)](https://learn.microsoft.com/en-us/previous-versions/windows/desktop/dnacc/understanding-sami-1.0)
    - [Universal Subtitle Format (USF)](https://en.wikipedia.org/wiki/Universal_Subtitle_Format)
    - [LyRiCs (LRC)](https://en.wikipedia.org/wiki/LRC_(file_format))
    - open an issue with "enhancement" label for more

## Examples

Read the [wiki](https://github.com/adfreelife/PyCaptions/wiki).

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

### Specific reader
Have the same functions as generic, except

```python
from pycaptions import SubRip, detectSRT

with open("tests/test.en.srt", encoding="UTF-8") as f:
    if detectSRT(f): # or SubRip.detect(f)
        captions = SubRip().read(f)
        captions.saveVTT("test")
```

### Multilingual
```python
from pycaptions import Captions

# if the format supports multiple languages
with Captions("tests/test.ttml") as captions:
    # first line will be in english, second one in spanish
    captions.saveSRT("test", ["en","es"]) 
    
# if you have multiple files and you want to make multilingual one
with Captions("tests/test.en.srt") as captions:
    with Captions("tests/test.es.srt") as captions2:
        # only subtitle text and comments (if format supports them) are added
        captions+=captions2 
    # first line will be in english, second one in spanish
    captions.save("test", ["en","es"]) 
```

### Combine files
```python
with Captions("tests/test.en.srt") as captions:
    captions.joinFile("tests/test.en.srt", add_end_time=True)
    captions.save("test")
```

## Changelog
### v0.5.2
Release date: 2024-01-24

Changes:
- Added `save_as` arguments to `toJson` function, can be of value `caption_array`, `dict`, `string`.
- Added `FileExtensions.getvars` that returns key-value pairs of variable names and extensions
- Added `BlockType.getvars` that returns key-value pairs of variable names and numbers
- `MicroDVD.read` now converts control code `H` value to language code
- `MicroDVD.read` now stores unimplemented/unknown control codes (json)
- Added `charset-normalizer` package so that `with` keyword and `fromJson`, `fromLegacyJson` can have `encoding="auto"`
- `with` keyword now supports loading legacy json with argument `legacyJson=True`

Fixes:
- Fixed an issue where `detectTTML` causes infinit loop.

Read past changes [here](https://github.com/adfreelife/PyCaptions/blob/main/CHANGELOG.md).