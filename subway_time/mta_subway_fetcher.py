from .utils import get_resource
import csv
import datetime
from google.transit import gtfs_realtime_pb2
import requests
from .nyct_subway_pb2 import *
import math

class MTASubwayFetcher:
    def __init__(self, api_key, feed_ids, stop_ids):
        self.api_key = api_key
        self.feed_ids = feed_ids
        self.stop_ids = stop_ids

    def fetch(self):
        stop_info = {}
        with open(get_resource("stops.csv"), "r") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['stop_id'] in self.stop_ids:
                    stop_info[row['stop_id']] = {"name": row['stop_name']}

        for feed_id in self.feed_ids:
            current_time = datetime.datetime.now()
            feed = gtfs_realtime_pb2.FeedMessage()
            response = requests.get("http://datamine.mta.info/mta_esi.php?key=%s&feed_id=%d" % (self.api_key, feed_id))
            feed.ParseFromString(response.content)
            for entity in feed.entity:
                if entity.trip_update:
                    for update in entity.trip_update.stop_time_update:
                        if update.stop_id in self.stop_ids:
                            stop_info[update.stop_id]["line"] = entity.trip_update.trip.route_id
                            nyct_extension = entity.trip_update.trip.Extensions[nyct_trip_descriptor]
                            stop_info[update.stop_id]["direction"] = self.get_direction(nyct_extension)
                            time = update.arrival.time
                            if time <= 0:
                                time = update.departure.time
                            time = datetime.datetime.fromtimestamp(time)
                            time = math.trunc(((time - current_time).total_seconds()) / 60)
                            times = stop_info[update.stop_id].get("next_train_times", [])
                            times.append(time)
                            stop_info[update.stop_id]["next_train_times"] = times
        return stop_info

    def get_direction(self, ext):
        return {ext.NORTH: "North",
                ext.EAST: "East",
                ext.SOUTH: "South",
                ext.WEST: "West"}[ext.direction]


