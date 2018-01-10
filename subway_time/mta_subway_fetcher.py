from subway_time.utils import get_resource
import csv
import datetime
from google.transit import gtfs_realtime_pb2
import requests
from subway_time.nyct_subway_pb2 import *
import math
import copy
import time
import threading


class MTASubwayFetcher:
    def __init__(self, api_key, feed_ids, stop_ids):
        self.api_key = api_key
        self.feed_ids = feed_ids
        self.stop_ids = stop_ids
        self.init_data = {}
        with open(get_resource("stops.csv"), "r") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                if row['stop_id'] in self.stop_ids:
                    self.init_data[row['stop_id']] = {"name": row['stop_name']}
        self.data = self.init_data
        self.fetch()
        t = threading.Thread(target=self.loop, daemon=True)
        t.start()

    def loop(self):
        while True:
            time.sleep(60)
            self.fetch()

    def fetch(self):
        stop_info = copy.deepcopy(self.init_data)
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
                            stop_info[update.stop_id]["direction"] = MTASubwayFetcher.get_direction(nyct_extension)
                            train_time = update.arrival.time
                            if train_time <= 0:
                                train_time = update.departure.time
                            train_time = datetime.datetime.fromtimestamp(train_time)
                            train_time = math.trunc(((train_time - current_time).total_seconds()) / 60)
                            times = stop_info[update.stop_id].get("next_train_times", [])
                            times.append(train_time)
                            stop_info[update.stop_id]["next_train_times"] = times

        self.data = stop_info

    @staticmethod
    def get_direction(ext):
        return {ext.NORTH: "North",
                ext.EAST: "East",
                ext.SOUTH: "South",
                ext.WEST: "West"}[ext.direction]
