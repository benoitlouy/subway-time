import time
import argparse
import sys
import json
from subway_time.data_provider import mta
from subway_time.utils import get_resource
from subway_time.display import sdl
from PIL import Image, ImageDraw, ImageFont
import math
from subway_time.tile import Tile


class Config:
    def __init__(self, path):
        with open(path, 'r') as config_file:
            config = json.load(config_file)

        self.feed_ids = config["mta"]["feed_ids"]
        self.api_key = config["mta"]["api_key"]
        self.stop_ids = config["mta"]["stop_ids"]


def get_image(tiles, width, height):
    image = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(image)
    for tile in tiles:
        if tile.x < width:
            tile.draw(draw)
    return image


displays = {
    "sdl": sdl.Display
}


def main():
    scale = 1
    fps = 10
    max_predictions = 3
    width = 64
    height = 16
    stop_name_template = "#FFFFFF{%(line)s %(name)s }#6E6E6E{%(direction)s}"

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--config", "-c", required=True)
    arg_parser.add_argument("--display", "-d", default="sdl")
    args = arg_parser.parse_args()

    config = Config(args.config)

    fetcher = mta.Fetcher(config.api_key, config.feed_ids, config.stop_ids, stop_name_template,
                          {5: "#FF0000", 10: "#FFFF00", 100000: "#00FF00"})

    font_path = get_resource("helvR08.pil")
    font = ImageFont.load(font_path)
    font_y_offset = -2

    display = displays[args.display](width * scale , height * scale)

    tile_width = font.getsize("88 min" * max_predictions + ", " * (max_predictions - 1))[0]

    w = font.getsize('No Predictions')[0]
    if w > tile_width:
        tile_width = w

    getters = []
    for stop_id in fetcher.data:
        getters.append(fetcher.get(stop_id))

    for stop_id in fetcher.data:
        label = fetcher.max_width_text(stop_id)
        w = font.getsize(label)[0]
        if w > tile_width:
            tile_width = w

    tile_width += 6

    if tile_width >= width:
        tiles_across = 2
    else:
        tiles_across = int(math.ceil(width / tile_width)) + 1

    tiles = []
    next_prediction = 0  # Index of predictList item to attach to tile
    for x in range(tiles_across):
        for y in range(0, height // 16):
            tiles.append(Tile(x * tile_width + y * tile_width / 2, y * 17, getters[next_prediction], font, font_y_offset))
            next_prediction = (next_prediction + 1) % len(getters)

    current_time = time.time()

    while True:
        previous_time = current_time
        image = get_image(tiles, width, height).resize((width * scale, height * scale))
        
        display.refresh(image)

        for tile in tiles:
            tile.x -= 1  # move tile to the left
            # if tile.x <= -tile_width:  # is tile off the left ledge
            if tile.x + tile.width <= 0:
                tile.x += tile_width * tiles_across  # move the tile back to right
                tile.getter = getters[next_prediction]  # assign next prediction to the tile
                next_prediction = (next_prediction + 1) % len(getters)  # cycle to the next prediction

        current_time = time.time()
        time_delta = (1.0 / fps) - (current_time - previous_time)
        if time_delta > 0.0:
            time.sleep(time_delta)


if __name__ == "__main__":
    sys.exit(main())
