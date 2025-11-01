from setuptools import setup, find_packages

setup(
    name="olympus",
    version="1.0.0",
    packages=find_packages(),
    py_modules=["run"],
    entry_points={
        "console_scripts": [
            "olympus=run:main",
        ],
    },
    python_requires=">=3.8",
)
