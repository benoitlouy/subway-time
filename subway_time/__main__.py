#!/usr/bin/env python

from google.transit import gtfs_realtime_pb2
import requests
from .nyct_subway_pb2 import *
import datetime
import math
from PIL import Image, ImageFont, ImageDraw
import csv
import json
import argparse
import os
import sys

def get_direction(ext):
    return {ext.NORTH: "North",
            ext.EAST: "East",
            ext.SOUTH: "South",
            ext.WEST: "West"}[ext.direction]

def minutes_to_text(time):
    if time == 0:
        return "now"
    else:
        return "%s min" % time

def get_resource(filename):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), filename)

class Config:
    def __init__(self, path):
        with open(path, 'r') as config_file:
            config = json.load(config_file)

        self.feed_ids = config["mta"]["feed_ids"]
        self.api_key = config["mta"]["api_key"]
        self.stop_ids = config["mta"]["stop_ids"]

def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--config", "-c", required = True)
    args = arg_parser.parse_args()

    config = Config(args.config)

    font_path = get_resource("helvR08.pil")
    font = ImageFont.load(font_path)
    stop_info = {}
    with open(get_resource("stops.csv"), "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['stop_id'] in config.stop_ids:
                stop_info[row['stop_id']] = {"name": row['stop_name']}

    for feed_id in config.feed_ids:
        current_time = datetime.datetime.now()
        feed = gtfs_realtime_pb2.FeedMessage()
        response = requests.get("http://datamine.mta.info/mta_esi.php?key=%s&feed_id=%d" % (config.api_key, feed_id))
        feed.ParseFromString(response.content)
        for entity in feed.entity:
            if entity.trip_update:
                for update in entity.trip_update.stop_time_update:
                    if update.stop_id in config.stop_ids:
                        stop_info[update.stop_id]["line"] = entity.trip_update.trip.route_id
                        nyct_extension = entity.trip_update.trip.Extensions[nyct_trip_descriptor]
                        stop_info[update.stop_id]["direction"] = get_direction(nyct_extension)
                        time = update.arrival.time
                        if time <= 0:
                            time = update.departure.time
                        time = datetime.datetime.fromtimestamp(time)
                        time = math.trunc(((time - current_time).total_seconds()) / 60)
                        times = stop_info[update.stop_id].get("next_train_times", [])
                        times.append(time)
                        stop_info[update.stop_id]["next_train_times"] = times

    print(stop_info)

    image = Image.new("RGB", (64, 32))
    draw = ImageDraw.Draw(image)
    i = 0
    for k, v in stop_info.items():
        text = "%(line)s %(direction)s" % v
        times_text = ", ".join([minutes_to_text(time) for time in v["next_train_times"]])
        draw.text((0,i*8-1), text + ": " + times_text, (200, 200, 200), font = font)
        i = i + 1

    image.save("out.ppm", "PPM")

if __name__ == "__main__":
    sys.exit(main())
