from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

setup(
        name="matrix-display",

        version="1.0.0",

        description="Application to display train arrival time on a RGB led matrix",

        packages = find_packages(exclude = ["contrib", "docs", "tests"]),
        
        install_requires=["pillow", "PySDL2"],

        python_requires=">=3",

        package_data = {
            "matrix_display": [
                "helvR08.pbm",
                "helvR08.pil"
                ]
        },

        entry_points={
            "console_scripts": [
                "matrix-display=matrix_display.__main__:main"
            ]
        }
)
