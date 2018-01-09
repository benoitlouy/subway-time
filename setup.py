from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

setup(
        name = "subway-time",

        version = "1.0.0",

        description = "Application to display train arrival time on a RGB led matrix",

        packages = find_packages(exclude = ["contrib", "docs", "tests"]),
        
        install_requires = ["pillow", "requests", "gtfs-realtime-bindings"],

        python_requires = ">=3",

        package_data = {
            "subway_time": [
                "stops.csv",
                "helvR08.pbm",
                "helvR08.pil"
                ]
        },

        entry_points = {
            "console_scripts": [
                "subway-time=subway_time.__main__:main"
            ]
        }
)
