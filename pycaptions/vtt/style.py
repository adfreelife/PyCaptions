@classmethod
def fromVTTunstyled(cls, text, pattern, options):
    pass

@classmethod
def fromVTT(cls, text, style):
    pass

def getVTT(self, lines:int = -1, options: dict = None,
           add_metadata: bool = True, **kwargs):
    self.format_lines(lines=lines, **kwargs)
    for tag in self.find_all():
        if tag.name:
            if tag.name == "br":
                if lines == 1:
                    tag.insert_before(" ")
                else:
                    tag.insert_before("\n")
                tag.unwrap()
    return self.get_text()
