from subway_time.utils import minutes_to_text


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
        self.getter = getter
        self.font = font
        self.font_y_offset = font_y_offset

    def __repr__(self):
        return "<Tile: x=%s y=%s data=%s>" % (self.x, self.y, self.getter())

    def draw(self, draw):
        data = self.getter()
        x = self.x
        label = data["line"] + ' ' + data["name"] + ' '  # Route number or code
        draw.text((x, self.y + self.font_y_offset), label, font=self.font, fill=Tile.route_color)
        x += self.font.getsize(label)[0]
        label = data["direction"]  # Route direction/desc
        draw.text((x, self.y + self.font_y_offset), label, font=self.font, fill=Tile.desc_color)
        x = self.x
        if not data["next_train_times"]:
            draw.text((x, self.y + self.font_y_offset + 8), 'No Predictions', font=self.font, fill=Tile.no_times_color)
        else:
            is_first_shown = True
            count = 0
            for p in data["next_train_times"]:
                if p <= Tile.shortTime:
                    fill = Tile.short_time_color
                elif p <= Tile.midTime:
                    fill = Tile.mid_time_color
                else:
                    fill = Tile.long_time_color
                if is_first_shown:
                    is_first_shown = False
                else:
                    # The comma between times needs to
                    # be drawn in a goofball position
                    # so it's not cropped off bottom.
                    label = ", "
                    draw.text((x + 1, self.y + self.font_y_offset + 8 - 2), label, font=self.font, fill=Tile.mins_color)
                    x += self.font.getsize(label)[0]
                label = minutes_to_text(p)
                draw.text((x, self.y + self.font_y_offset + 8), label, font=self.font, fill=fill)
                x += self.font.getsize(label)[0]
                count += 1
                if count >= Tile.maxPredictions:
                    break
