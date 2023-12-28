import json, textwrap, budoux, io, os
from collections import defaultdict 
from langcodes import standardize_tag, tag_is_valid

EXTENSION = None

class BlockType:
    CAPTION = 1
    COMMENT = 2
    STYLE = 3
    LAYOUT = 4
    METADATA = 5

class Block:
    def __init__(self, block_type: int, lang: str = "und", start_time: int = 0, end_time: int = 0, text: str = "", **options):
        self.block_type = block_type
        self.languages = defaultdict(str)
        self.default_language = lang
        if(text):
            self.languages[lang] = text.strip()
        self.start_time = start_time
        self.end_time = end_time
        self.options = options or {}

    def __getitem__(self, index: str):
        return self.languages[index]
    
    def __setitem__(self, index: str, value: str):
        self.languages[index] = value

    def getLines(self, lang: str, lines: int) -> list[str]:
        text = self.get(lang)
        if lang == "ja":
            parser = budoux.load_default_japanese_parser()
            return parser.parse(text)
        elif lang in ["zh","zh-CN","zh-SG","zh-Hans"]:
            parser = budoux.load_default_simplified_chinese_parser()
            return parser.parse(text)
        elif lang in ["zh-HK", "zh-MO", "zh-TW", "zh-Hant"]:
            parser = budoux.load_default_simplified_chinese_parser()
            return parser.parse(text)
        else:
            return textwrap.wrap(text)
    
    def get(self, lang: str) -> str:
        return self.languages.get(lang)
    
    def append(self, text: str, lang: str):
        if not self.default_language:
            self.default_language = lang
        if lang not in ["ja","zh","zh-CN","zh-SG","zh-Hans","zh-HK", "zh-MO", "zh-TW", "zh-Hant"]:
            self.languages[lang] += " " + text.strip()
        else:
            self.languages[lang] += text

    def shift_time(self, duration: int):
        self.start_time += duration
        self.end_time += duration

    def shift_start(self, duration: int):
        self.start_time += duration

    def shif_end(self, duration: int):
        self.end_time += duration

    def __str__(self):
        temp = '\n'.join(f" {lang}: {text}" for lang, text in self.languages.items())
        return f"start: {self.start_time} end: {self.end_time}\n{temp}"
    
    def __iadd__(self, value):           
        if not isinstance(value, Block):
            raise ValueError("Unsupported type. Must be an instance of `Block`")
        for key, language in value:
            self.languages[key] = language
        return self

    def __add__(self, value):
        if not isinstance(value, Block):
            raise ValueError("Unsupported type. Must be an instance of `Block`")
        out = Block(start_time=self.start_time,end_time=self.end_time,lang=self.default_language,style=self.style,layout=self.layout,is_chapter=self.is_chapter)
        out.languages = self.languages.copy()
        for key, language, comment in value:
            out.languages[key] = language
        return out
    
    def __isub__(self, language: str):
        if language in self.languages:
            del self.languages[language]
        return self

    def __sub__(self, language: str):
        out = Block(start_time=self.start_time,end_time=self.end_time,lang=self.default_language,style=self.style,layout=self.layout,is_chapter=self.is_chapter)
        out.languages = self.languages.copy()
        if language in out.languages:
            del out.languages[language]
        return out

    def __iter__(self):
        self._keys_iterator = iter(self.languages)
        return self
    
    def __next__(self):
        try:
            key = next(self._keys_iterator)
            return key, self.languages.get(key)
        except StopIteration:
            raise StopIteration
  
class CaptionsFormat:
    EXTENSION = EXTENSION
    def getExtension(self): 
        return self.EXTENSION 

    def __init__(self, filename: str = None, default_language: str = "und", **options):
        self.filename = filename
        self.options = options or {}
        self._block_list: list[Block] = []
        self.setDefaultLanguage(default_language)

    def setDefaultLanguage(self, language: str):
        standardized = standardize_tag(language, macro=True)
        self.default_language = standardized if(tag_is_valid(standardized)) else "und"

    def __getitem__(self, index: int):
        return self._block_list[index]
    
    def __setitem__(self, index: int, value: Block):
        self._block_list[index] = value

    def insert(self, index: int, value: Block):
        self._block_list.insert(index,value)

    def __iadd__(self, value):
        if not isinstance(value, CaptionsFormat):
            raise ValueError("Unsupported type. Must be an instance of `CaptionsFormat`")
        for i, value in enumerate(value):
            if i<len(self._block_list):
                self._block_list[i] += value
            else:
                self.append(value)
        return self

    def __isub__(self, language: str):
        for value in self._block_list:
            value -= language
        return self

    def __iter__(self):
        return iter(self._block_list)

    def __str__(self):
        return "\n".join(f"{i}. {caption}" for i,caption in enumerate(self._block_list))
    
    def detect(self, file: str | io.IOBase = None):
        raise ValueError("Not implemented")
    
    def _read(self, content: str | io.IOBase, lang: str = None, **kwargs):
        raise ValueError("Not implemented")
    
    def read(self, content: str | io.IOBase, lang: str = None, **kwargs):
        self._read(content,lang,**kwargs)

    def _save(self, filename: str, lang: str = None, **kwargs):
        raise ValueError("Not implemented")
    
    def save(self, filename: str, lang: str = None, **kwargs):
        languages = languages or [self.default_language]
        if not filename.endswith(self.getExtension()):
            filename += self.getExtension()

        for i in languages:
            if i not in filename:
                file, ext = os.path.splitext(filename)
                filename = f"{file}.{i}{ext}"

        self._save(filename, lang, **kwargs)

    def __len__(self):
        return len(self._block_list)
    
    def __enter__(self):
        filename, ext = os.path.splitext(self.filename)
        filename, lang = os.path.splitext(filename)
        if(lang):
            self.setDefaultLanguage(lang[1:])
        if(ext == ".json"):
            self.fromJson(self.filename)
        else:
            with open(self.filename,"r",encoding="UTF-8") as stream:
                if self.detect(stream):
                    self._read(stream)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def append(self, item: Block):
        self._block_list.append(item)

    def shift_time(self, duration: int):
        for i in self:
            i.shift_time(duration)

    def shift_start(self, duration: int):
        for i in self:
            i.shift_start(duration)

    def shif_end(self, duration: int):
        for i in self:
            i.shif_end(duration)

    def fromJson(self, file: str):
        try:
            with open(file,"r",encoding = "UTF-8") as f:
                data = json.load(f)
                self.default_language = data["default_language"]
                for key, caption in data["_caption_list"].items():
                    self._block_list = [Block(**item) for item in caption]
        except IOError as e:
            print(f"I/O error({e.errno}): {e.strerror}")
        except Exception as e:
            print(f"Error {e}")

    def toJson(self, file: str):
        try:
            with open(file,"w",encoding="UTF-8") as f:
                if len(self._block_list) == 1 or self.default_language not in self._block_list:
                    default_language = next(iter(self._block_list.keys()))
                else:
                    default_language = self.default_language
                json.dump({"default_language" : default_language, "_caption_list" : self._block_list}, f, default=vars)
        except IOError as e:
            print(f"I/O error({e.errno}): {e.strerror}")
        except Exception as e:
            print(f"Error {e}")
    