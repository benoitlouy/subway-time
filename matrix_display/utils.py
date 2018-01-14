import os


def get_resource(filename, f):
    return os.path.join(os.path.dirname(os.path.realpath(f)), filename)


