from setuptools import setup

setup(
    name="olympus",
    version="1.0.0",
    py_modules=["run_windows"],
    entry_points={
        "console_scripts": [
            "olympus=run_windows:main",
        ],
    },
)
