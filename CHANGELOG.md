Table of Contents
- [v0.7.0 [stable]](#v070)
- [v0.6.0 [stable]](#v060)
- [v0.5.2 [stable]](#v052)
- [v0.5.1](#v051)
- [v0.5.0](#v050)
- [v0.4.1 [stable]](#v041)
- [v0.4.0](#v040)
- [v0.3.1](#v031)
- [v0.3.0](#v030)
- [v0.2.2](#v022)
- [v0.2.1 [broken]](#v021)

### v0.7.0
Release date: 2024-02-06
<br>Commit: [fdfed84](https://github.com/adfreelife/PyCaptions/commit/fdfed842ea43de1484d7b1367d001a3159edede3)

Changes:
- **Added cli support** (e.g `pycaptions "path/to/file/file.srt" -f vtt`)
- Added autoformat for all values of `lines`
- Added function `CaptionsFormat.getLanguagesAndFilename`
- Added function `CaptionsFormat.getFilename`
- Added `MicroTime.fromMicrotime` creates a MicroTime from a list
- Added `MicroTime.toMicrotime` returns a MicroTime as a list
- Added `MicroTime.fromAnyFormat` returns a MicroTime from provided format (case insensitive)
- `MicroTime.fromSUBTime` and `MicroTime.toSUBTime` now supports framerate as string
- `Captions.save` output_format is now case insensitive
- Improved MicroDVD style conversion
- Internal restructure for faster development
- Invalid `style` argument will result in `style=None`
- Added `style_options` for changing style globaly, default `style="full"` `lines=-1`, this affects how the style is parsed. (e.g. `style_options.style=None` and then using argument `style="full"` will not convert any style due to optimizations for faster conversion)
- Hypens at the end of the lines (e.g "Some-<br/>thing") will be removed if `lines` is >-1
- `Styling` is now split into `StyleFormat` and `Styling(StyleFormat)`

Fixes:
- Fixed "lxml is not installed" error
- Fixed `Styling.getTTML` converting invalid css properties into ttml properties. To-do: add value checks for these properties.
- Fixed `CaptionsFormat.getLanguagesFromFilename` getting languages from directory path (e.g. `\path.to.file\file.en.srt` -> `["to", "en"]`)
- Fixed width and height not being saved to json

### v0.6.0
Release date: 2024-01-26
<br>Commit: [0fb361f](https://github.com/adfreelife/PyCaptions/commit/0fb361f69b71c4854ab72623d00d0002bdce3076)

Changes:
- Added support for inline style conversion for MicroDVD
- Added `style` argument to readers, possible values `None` (no styling), default `full` (converts inline styles only for now)
- Added `lines` argument to readers, possible values default `-1` (preserves original), `0` (automatically determins number of lines, works only with `style=None` for now), `1` (fits everything in one line), `n` (positive integer bigger than 1, fits text into `n` lines, works only with `style=None` for now)
- Removed `no_styling` argument, replaced by `style=None`
- Renamed `Block.getLines` to `Block.get_lines`
- TTML writer now writes multilingual files the same way as other writers by default, add `mark_language_type=True` to make it write the same as before
- Added dependency for `webcolors` to transform web color names to hex colors
- Added decorators `@captionsDetector`, `@captionsReader`, `@captionsWriter` for better code structure
- Added `MicroTime.recalculate` to recalculate time into the right values (e.g. 99min -> 1h 39min)
- Moved `CaptionsFormat.checkContent` and `CaptionsFormat.getGenerator` to decorators that used them
- Added `Captions.detectors` and improved `Captions.get_format` method

Fixes:
- Fixed `detectTTML` not seeking file to the original offset
- Fixed `MicroTime.fromTTMLTime` returning 0 instead of infinity if no valid values are provided
- Fixed `TTML.reader` not adding section time to end block time
- Fixed `Block.copy` not returning a deepcopy of itself
- Fixed `Block` substraction and addition not using `Block.copy`

### v0.5.2
Release date: 2024-01-24
<br>Commit: [cf59a36](https://github.com/adfreelife/PyCaptions/commit/cf59a3645df0ee1f888e5d6e79d38e2eb1604b86)

Changes:
- Added `save_as` arguments to `toJson` method, can be of value `caption_array`, `dict`, `string`.
- Added `FileExtensions.getvars` that returns key-value pairs of variable names and extensions
- Added `BlockType.getvars` that returns key-value pairs of variable names and numbers
- `MicroDVD.read` now converts control code `H` value to language code
- `MicroDVD.read` now stores unimplemented/unknown control codes (json)
- Added `charset-normalizer` package so that `with` keyword and `fromJson`, `fromLegacyJson` can have `encoding="auto"`
- `with` keyword now supports loading legacy json with argument `legacyJson=True`

Fixes:
- Fixed an issue where `detectTTML` can cause an infinit loop if there is one or less lines in a file.

### v0.5.1
Release date: 2024-01-23
<br>Commit: [39aa066](https://github.com/adfreelife/PyCaptions/commit/39aa06659bff25367f6cefe5f5c1116047104119)

Changes:
- Added `fromLegacyJson` to parse json saved before version v0.5.0
- Added `identifier: pycaptions` and `version` to json if something changes in the future.
- `Block` of type `BlockType.STYLE` now parses `options.style` if it's a string by default when initialized, otherwise use `styling.cssParser` or `cssutils.CSSParser` to parse css beforehand.
- You can now change save extensions globaly by `save_extensions.{format} = {str}`

Fixes:
- Fixed `toJson` not saving correctly due to atribute rename
- Fixed `cssutils.css.CSSStyleSheet` causing error when using `toJson`
- Fixed `CaptionsFormat.getLayout` not returning `Block`
- Fixed `CaptionsFormat.getStyle` not returning `Block` 
- Fixed `CaptionsFormat.getMetadata` not returning `Block` 

### v0.5.0
Release date: 2024-01-21
<br>Commit: [0cef8bd](https://github.com/adfreelife/PyCaptions/commit/0cef8bd36805dde5a58323f309754fc745f50f51)

Changes:
- SRT writer optimization
- Keyword `with` now supports string/iostream with parameter `isFile = False`
- budoux version upgrade for Thai formating support
- `languages`` is now not required parameter for readers
- Added basic ttml writer
- `detectTTML` now detects valid xml with empty lines
- Changed `CaptionsFormat.getLayout` to `CaptionsFormat.getLayoutById`, original now returns a list
- Changed `CaptionsFormat.getStyle` to `CaptionsFormat.getStyleById`, original now returns a list
- Changed `CaptionsFormat.getMetadata` to `CaptionsFormat.getMetadataById`, original now returns a list
- Added `CaptionsFormat.removeComments`, `CaptionsFormat.removeOptionsComments`, `CaptionsFormat.removeAllComments` for removing comment blocks
- Implemented `Block.getLines` that returns text in specified number of lines without style.

### v0.4.1
Release date: 2024-01-14
<br>Commit: [1c05f58](https://github.com/adfreelife/PyCaptions/commit/1c05f58bacccb1ef147461a6f0a644168ff71db1)

Changes:
- Removed a print line in MicroDVD
- Renamed `supported_reader` to `supported_readers`

### v0.4.0
Release date: 2024-01-14
<br>Commit: [335964e](https://github.com/adfreelife/PyCaptions/commit/335964ec69d6a623410f37eb9f94a0d8ca578f06)

Changes:
- Added styling class that will convert from and to specific format
- Added `supported_reader` so you can get extensions for all supported readers
- `supported_extensions` now only gives extensions for writers

Fixes:
- Fixed `time_offset` being set to 0 instead of MicroTime in readers
- Fixed `MicroTime.fromVTTTime` not converting strings to integers
- Fixed `CaptionsFormat.append` not working if no end time is provided in a block
- Fixed `Captions.save` not working without providing output format


### v0.3.1
Release date: 2024-01-10
<br>Commit: [081f073](https://github.com/adfreelife/PyCaptions/commit/081f073a4867b0b0bbabdbe881c0c5050deb3721)

Changes:
- Added `Block.append_without_common_part`

### v0.3.0
Release date: 2024-01-10
<br>Commit: [710c8be](https://github.com/adfreelife/PyCaptions/commit/710c8be449f64a572649f7bcaf3a21fe28149e64)

Changes:
- Added MicroDVD writer
- Extended SRT support
- `Captions.save` now works when providing output format with "." prefix


### v0.2.2
Release date: 2024-01-07
<br>Commit: [1f35853](https://github.com/adfreelife/PyCaptions/commit/1f35853f4cb74d19b057abf671356d8e4f2bbbeb)

Changes:
- Implemented `WebVTT.save`

Fixes:
- Fixed imports

### v0.2.1
Release date: 2024-01-07
<br>Commit: [3dc02be](https://github.com/adfreelife/PyCaptions/commit/1f35853f4cb74d19b057abf671356d8e4f2bbbeb)

Initial release
- Supported readers: SubRip, WebVTT, MicroDVD, TTML
- Supported writers: SubRip

