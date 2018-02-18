import datetime
import functools
from matrix_display.color_string import ColorString
import pytz


class DataProvider:
    def __init__(self, id, date_format="", time_format="", time_zone=None):
        self.id = id
        self.date_format = date_format
        self.time_format = time_format
        if time_zone:
            self.time_zone = pytz.timezone(time_zone)
        else:
            self.time_zone = None

    def access(self):
        now = datetime.datetime.now()
        if self.time_zone:
            now = self.time_zone.localize(now)
            # now = now.astimezone(self.time_zone)
        return [ColorString(now.strftime(self.date_format)), ColorString(now.strftime(self.time_format))]

    def get(self):
        return [(self.id, functools.partial(self.access))]
