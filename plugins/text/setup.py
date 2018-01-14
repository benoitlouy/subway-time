from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

setup(
        name="matrix-display-text-plugin",

        version="1.0.0",

        description="Text plugin for matrix display application",

        package_dir={
            "matrix_display_text_plugin": "src"
        },

        packages=["matrix_display_text_plugin"],
        
        install_requires=[],

        python_requires=">=3"
)
