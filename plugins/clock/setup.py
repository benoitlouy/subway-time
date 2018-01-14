from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

setup(
        name="matrix-display-clock-plugin",

        version="1.0.0",

        description="Clock plugin for matrix display application",

        package_dir={
            "matrix_display_clock_plugin": "src"
        },

        packages=["matrix_display_clock_plugin"],
        
        install_requires=["pytz"],

        python_requires=">=3"
)
