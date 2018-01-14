from subway_time.color_string import ColorString
import functools


class Fetcher:
    def __init__(self, id, header="", text=""):
        self.id = id
        self.header = ColorString(header)
        self.text = ColorString(text)
        self.i = 0

    def access(self):
        return [self.header, self.text]

    def dummy(self):
        return [ColorString("#FF00FF{FOO}"), ColorString("#FF00FF{BAR}")]

    def get(self):
        self.i += 1
        print(self.i)
        if self.i < 300 or self.i > 600:
            return [(self.id, functools.partial(self.access)),]
        else:
            print("FOO")
            return [(self.id, functools.partial(self.access)), (self.id + "foo", functools.partial(self.dummy))]
