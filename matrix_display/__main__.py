import time
import argparse
import sys
import json
from .utils import get_resource
from PIL import Image, ImageDraw, ImageFont
from .tile import Tile
import importlib
from itertools import groupby


def get_image(tiles, width, height):
    image = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(image)
    for row in tiles:
        for tile in row:
            if tile.x + tile.width >= 0 and tile.y < height:
                tile.draw(draw)
    return image


def load_fetchers(config):
    fetchers = [(fetcher_config["row"], importlib.import_module(fetcher_config["module"]).DataProvider(fetcher_id, **fetcher_config["config"]))
                for fetcher_id, fetcher_config in config["fetchers"].items()]
    result = {}
    for fetcher_id, fetcher in fetchers:
        row = result.get(fetcher_id, [])
        result[fetcher_id] = row
        row.append(fetcher)
    return result


def load_displays(config):
    displays = {}
    for display_id, display_config in config["displays"].items():
        displays[display_id] = importlib.import_module(display_config["module"]).Display(**display_config["config"])
    return displays

def refresh_getters(fetchers, getters):
    for row_num, row_fetchers in fetchers.items():
        row_getters = getters.get(row_num, [])
        getters[row_num] = row_getters
        # removing old getters
        to_remove = []
        new_getters = []
        for fetcher in row_fetchers:
            new_getters.extend(fetcher.get())
        updated_getters = dict(new_getters)
        updated_getter_ids = updated_getters.keys()
        for idx, row_getter in enumerate(row_getters):
            if row_getter[0] not in updated_getter_ids:
                to_remove.append(idx)
        for offset, idx in enumerate(to_remove):
            del row_getters[idx - offset]
        # adding new getters
        current_row_getters_id = [row_getter[0] for row_getter in row_getters]
        for k, v in updated_getters.items():
            if k not in current_row_getters_id:
                row_getters.append((k, v))


def main():
    width = 64
    height = 32

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--config", "-c", required=True)
    arg_parser.add_argument("--display", "-d", default="sdl")
    arg_parser.add_argument("--fps", "-f", type=int, default=20)
    args = arg_parser.parse_args()

    with open(args.config, 'r') as config_file:
        config = json.load(config_file)

    fps = args.fps

    # init data providers
    fetchers = load_fetchers(config)
    getters = {}
    refresh_getters(fetchers, getters)

    # init font
    font_path = get_resource("helvR08.pil", __file__)
    font = ImageFont.load(font_path)
    font_y_offset = -2

    # init displays
    displays = load_displays(config)
    display = displays[args.display]

    # init tiles
    tile_padding = 10
    tiles = []
    for row_y in range(0, max(getters.keys()) + 1):
        tiles.append([])
        x = 0
        if row_y not in getters or len(getters[row_y]) == 0:
            continue
        while x < width:
            getter = getters[row_y].pop(0)
            getters[row_y].append(getter)
            tile = Tile(x, row_y * 17, getter[1], font, font_y_offset)
            tiles[row_y].append(tile)
            x += tile.width + tile_padding

    # main UI loop
    current_time = time.time()
    while True:
        previous_time = current_time
        image = get_image(tiles, width, height)
        display.refresh(image)
        refresh_getters(fetchers, getters)
        for row_y, row in enumerate(tiles):
            tiles_to_remove = []
            row_len = len(row)
            for idx, tile in enumerate(row):
                tile.x -= 1
                if idx == row_len - 1 and tile.x + tile.width + tile_padding < width:
                    getter = getters[row_y].pop(0)
                    getters[row_y].append(getter)
                    new_tile = Tile(tile.x + tile.width + tile_padding, row_y * 17, getter[1], font, font_y_offset)
                    row.append(new_tile)
                if idx == 0 and tile.x + tile.width < 0:
                    tiles_to_remove.append(idx)

            for offset, idx in enumerate(tiles_to_remove):
                del row[idx - offset]

        current_time = time.time()
        time_delta = (1.0 / fps) - (current_time - previous_time)
        if time_delta > 0.0:
            time.sleep(time_delta)
        current_time = time.time()


if __name__ == "__main__":
    sys.exit(main())
