import time
import argparse
import sys
import json
from subway_time.data_provider import mta
from subway_time.utils import get_resource
from subway_time.display import sdl
from PIL import Image, ImageDraw, ImageFont
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
    for row in tiles:
        for tile in row:
            if tile.x + tile.width >= 0:
                tile.draw(draw)
    return image


displays = {
    "sdl": sdl.Display
}


def main():
    scale = 1
    fps = 10
    width = 512
    height = 32
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

    display = displays[args.display](width * scale, height * scale)

    getters = [fetcher.get(stop_id) for stop_id in fetcher.data]

    tile_padding = 10

    tiles = [[]] * (height // 16)
    x = 0
    y = 0
    next_data_index = 0
    while x < width:
        tile = Tile(x, y, getters[next_data_index], font, font_y_offset)
        tiles[y].append(tile)
        x += tile.width + tile_padding
        next_data_index = (next_data_index + 1) % len(getters)

    current_time = time.time()
    while True:
        previous_time = current_time
        image = get_image(tiles, width, height).resize((width * scale, height * scale))
        display.refresh(image)

        for row in tiles:
            tiles_to_remove = []
            row_len = len(row)
            for idx, tile in enumerate(row):
                tile.x -= 1
                if idx == row_len - 1 and tile.x + tile.width + tile_padding < width:
                    new_tile = Tile(tile.x + tile.width + tile_padding, tile.y, getters[next_data_index], font, font_y_offset)
                    row.append(new_tile)
                    tile.add = True
                    next_data_index = (next_data_index + 1) % len(getters)
                if idx == 0 and tile.x + tile.width < 0:
                    tiles_to_remove.append(idx)

            for offset, idx in enumerate(tiles_to_remove):
                del row[idx - offset]

        current_time = time.time()
        time_delta = (1.0 / fps) - (current_time - previous_time)
        if time_delta > 0.0:
            time.sleep(time_delta)


if __name__ == "__main__":
    sys.exit(main())
