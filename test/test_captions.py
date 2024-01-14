from pycaptions import Captions, supported_extensions

test_file_path = "test/captions/"

for filename in ["test.en.srt", "test.en.sub", "test.en.vtt", "test.ttml"]:
    with Captions(test_file_path+filename) as c:
        for ext in supported_extensions:
            c.save(f"tmp/from_{filename.split('.')[-1]}", output_format=ext)

