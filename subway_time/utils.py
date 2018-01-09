import os

def minutes_to_text(time):
    if time == 0:
        return "now"
    else:
        return "%s min" % time

def get_resource(filename):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), filename)


