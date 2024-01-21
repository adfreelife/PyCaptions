Table of Contents
- [v0.5.0](#v050)
- [v0.4.1](#v041)
- [v0.4.0](#v040)
- [v0.3.1](#v031)
- [v0.3.0](#v030)
- [v0.2.2](#v022)
- [v0.2.1](#v021)

* * *
### v0.5.0
Release date: TBA
<br>Commit: [TBA]()

Changes:
- SRT writer optimization
- Keyword `with` now supports string/iostream with parameter `isFile = False`
- budoux version upgrade for Thai formating support

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
<br>Commit: [1f35853](https://github.com/adfreelife/PyCaptions/commit/1f35853f4cb74d19b057abf671356d8e4f2bbbeb)

Initial release
- Supported readers: SubRip, WebVTT, MicroDVD, TTML
- Supported writers: SubRip

