class Tile:
    def __init__(self, x, y, getter, font, font_y_offset):
        self.x = x
        self.y = y
        self.width = 0
        self.getter = getter
        self.font = font
        self.font_y_offset = font_y_offset
        self.data = None
        self.refresh()

    def __repr__(self):
        return "<Tile: x=%s y=%s>" % (self.x, self.y)

    def refresh(self):
        self.data = self.getter()
        right = 0
        for line in self.data:
            x = self.x
            for token in line.tokens:
                x += self.font.getsize(token.text)[0]
            right = max(right, x)
        self.width = right - self.x

    def draw(self, draw):
        for idx, line in enumerate(self.data):
            x = self.x
            for token in line.tokens:
                text = token.text
                color = token.color
                draw.text((x, self.y + self.font_y_offset + 7 * idx), text, font=self.font, fill=color)
                x += self.font.getsize(text)[0]
