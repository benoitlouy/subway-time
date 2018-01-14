from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

setup(
        name="matrix-display-mta-subway-plugin",

        version="1.0.0",

        description="MTA subway time plugin for matrix display application",

        package_dir={
            "matrix_display_mta_subway_plugin": "src"
        },

        packages=["matrix_display_mta_subway_plugin"],
        
        install_requires=["requests", "gtfs-realtime-bindings"],

        python_requires=">=3",

        package_data={
            "matrix_display_mta_subway_plugin": [
                "stops.csv"
            ]
        }
)
