class Tile:
    route_color = (255, 255, 255)  # Color for route labels (usu. numbers)
    desc_color = (110, 110, 110)  # " for route direction/description
    long_time_color = (0, 255, 0)  # Ample arrival time = green
    mid_time_color = (255, 255, 0)  # Medium arrival time = yellow
    short_time_color = (255, 0, 0)  # Short arrival time = red
    mins_color = (110, 110, 110)  # Commans and 'minutes' labels
    no_times_color = (0, 0, 255)  # No predictions = blue

    maxPredictions = 3  # NextBus shows up to 5; limit to 3 for simpler display
    minTime = 0  # Drop predictions below this threshold (minutes)
    shortTime = 5  # Times less than this are displayed in red
    midTime = 10  # Times less than this are displayed yellow

    def __init__(self, x, y, getter, font, font_y_offset):
        self.x = x
        self.y = y
        self.width = 0
        self.getter = getter
        self.font = font
        self.font_y_offset = font_y_offset

    def __repr__(self):
        return "<Tile: x=%s y=%s>" % (self.x, self.y)

    def draw(self, draw):
        data = self.getter()

        right = 0
        for idx, line in enumerate(data):
            x = self.x
            for token in line.tokens:
                text = token.text
                color = token.color
                draw.text((x, self.y + self.font_y_offset + 8 * idx), text, font=self.font, fill=color)
                x += self.font.getsize(text)[0]
            right = max(right, x)
        self.width = right - self.x
