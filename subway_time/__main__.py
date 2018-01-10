import time
import argparse
import sys
import json
from subway_time.mta_subway_fetcher import MTASubwayFetcher
from subway_time.utils import get_resource
from PIL import ImageFont
import math
from subway_time.tile import Tile

class Config:
    def __init__(self, path):
        with open(path, 'r') as config_file:
            config = json.load(config_file)

        self.feed_ids = config["mta"]["feed_ids"]
        self.api_key = config["mta"]["api_key"]
        self.stop_ids = config["mta"]["stop_ids"]


def main():
    fps = 1
    max_predictions = 3
    width = 64
    height = 32
    stop_name_template = "%(line)s %(name)s %(direction)s"

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--config", "-c", required = True)
    args = arg_parser.parse_args()

    config = Config(args.config)

    fetcher = MTASubwayFetcher(config.api_key, config.feed_ids, config.stop_ids)

    font_path = get_resource("helvR08.pil")
    font = ImageFont.load(font_path)

    # compute tile width
    tile_width = font.getsize("88 min" * max_predictions + ", " * (max_predictions - 1))[0]

    w = font.getsize('No Predictions')[0]
    if w > tile_width:
        tile_width = w

    getters = []
    for stop_id in fetcher.data:
        getters.append(fetcher.get(stop_id))

    for getter in getters:
        label = stop_name_template % getter()
        w = font.getsize(label)[0]
        if w > tile_width:
            tile_width = w

    tile_width += 6

    if tile_width >= width:
        tiles_across = 2
    else:
        tiles_across = int(math.ceil(width / tile_width)) + 1

    tile_list = []
    next_prediction = 0  # Index of predictList item to attach to tile
    for x in range(tiles_across):
        for y in range(0, 2):
            tile_list.append(Tile(x * tile_width + y * tile_width / 2, y * 17, getters[next_prediction]))
            next_prediction += 1
            if next_prediction >= len(getters):
                next_prediction = 0

    print(tile_list)

    previous_time = time.time()
    while True:
        current_time = time.time()
        time_delta = (1.0 / fps) - (current_time - previous_time)
        if time_delta > 0.0:
            time.sleep(time_delta)
        previous_time = current_time


if __name__ == "__main__":
    sys.exit(main())
