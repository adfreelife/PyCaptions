import unittest
import json
from pycaptions import Captions, supported_extensions


IGNORE_JSON_FIELDS = ["filename"]
JSON_FIELDS = ["identifier", "json_version", "default_language", "time_length", "filename", "file_extensions", "options", "block_list"]
TEST_FILES_PATH = "test/captions/"
TEST_FILES = ["test.en.srt", "test.en.sub", "test.en.vtt", "test.ttml"]


class TestCaptions(unittest.TestCase):

    def check_json_fields(self, file_path):
        with open(file_path) as f:
            data = json.load(f)
        
        for i in JSON_FIELDS:
            self.assertIn(i, data)

        self.assertGreater(len(data["block_list"]),0)

    def compare_json_ignore_field(self, file1_path, file2_path, ignored_fields):
        with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
            data1 = json.load(file1)
            data2 = json.load(file2)

        # Remove the specified field from both dictionaries
        for field in ignored_fields:
            data1.pop(field)
            data2.pop(field)

        self.assertEqual(data1, data2)

    def test_all(self):
        for filename in TEST_FILES:
            with Captions(TEST_FILES_PATH+filename) as c:
                for ext in supported_extensions:
                    c.save(f"tmp/from_{filename.split('.')[-1]}", output_format=ext)
                c.toJson(f"tmp/from_{filename.split('.')[-1]}")
                self.check_json_fields(f"tmp/from_{filename.split('.')[-1]}.json")

    def test_json_to_json(self):
        for filename in TEST_FILES:
            _in = f"tmp/from_{filename.split('.')[-1]}.json"
            _out = f"tmp/from_{filename.split('.')[-1]}_json.json"
            with Captions(_in) as c:
                c.toJson(_out)
                self.compare_json_ignore_field(_in, _out, IGNORE_JSON_FIELDS)


if __name__ == '__main__':
    unittest.main()