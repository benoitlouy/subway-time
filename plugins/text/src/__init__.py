from matrix_display.color_string import ColorString
import functools


class DataProvider:
    def __init__(self, id, header="", text=""):
        self.id = id
        self.header = ColorString(header)
        self.text = ColorString(text)

    def access(self):
        return [self.header, self.text]

    def get(self):
        return [(self.id, functools.partial(self.access)),]
