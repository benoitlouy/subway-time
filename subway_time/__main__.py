import time
import argparse
import sys
import json
from subway_time.mta_subway_fetcher import MTASubwayFetcher
from subway_time.utils import get_resource
from PIL import ImageFont


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

    for stop_id, stop_data in fetcher.data.items():
        label = stop_name_template % stop_data
        w = font.getsize(label)[0]
        if w > tile_width:
            tile_width = w

    tile_width += 6

    previous_time = time.time()
    while True:
        current_time = time.time()
        time_delta = (1.0 / fps) - (current_time - previous_time)
        if time_delta > 0.0:
            time.sleep(time_delta)
        previous_time = current_time


if __name__ == "__main__":
    sys.exit(main())
