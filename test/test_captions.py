from pycaptions import Captions, supported_extensions

with Captions("test/captions/test.en.vtt") as c:
    for i in supported_extensions:
        c.save("tmp/out", output_format=i)

