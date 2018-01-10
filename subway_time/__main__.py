from PIL import Image, ImageFont, ImageDraw
import argparse
import os
import sys
import json
from .mta_subway_fetcher import MTASubwayFetcher
from .utils import get_resource, minutes_to_text

class Config:
    def __init__(self, path):
        with open(path, 'r') as config_file:
            config = json.load(config_file)

        self.feed_ids = config["mta"]["feed_ids"]
        self.api_key = config["mta"]["api_key"]
        self.stop_ids = config["mta"]["stop_ids"]

def main():

    fps = 1

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--config", "-c", required = True)
    args = arg_parser.parse_args()

    config = Config(args.config)

    font_path = get_resource("helvR08.pil")
    font = ImageFont.load(font_path)
    fetcher = MTASubwayFetcher(config.api_key, config.feed_ids, config.stop_ids)

    while True:
    stop_info = fetcher.fetch()

    print(stop_info)

    # image = Image.new("RGB", (64, 32))
    # draw = ImageDraw.Draw(image)
    # i = 0
    # for k, v in stop_info.items():
    #     text = "%(line)s %(direction)s" % v
    #     times_text = ", ".join([minutes_to_text(time) for time in v["next_train_times"]])
    #     draw.text((0,i*8-1), text + ": " + times_text, (200, 200, 200), font = font)
    #     i = i + 1

    # image.save("out.ppm", "PPM")

if __name__ == "__main__":
    sys.exit(main())
