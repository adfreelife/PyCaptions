import copy

def styleGetter(func):
    def wrapper(self, lines:int = -1, options: dict =  None, 
                add_metadata: bool = True, **kwargs):
        if self.lines_count != lines:
            self.format_lines(lines=lines, **kwargs)
        self.lines_count = lines
        return func(copy.copy(self), lines, options, add_metadata, **kwargs)
    return wrapper