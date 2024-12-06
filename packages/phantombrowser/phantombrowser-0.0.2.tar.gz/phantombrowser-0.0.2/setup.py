#!/usr/bin/env python
from setuptools import setup
from os import path


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md")) as f:
    long_description = f.read()

requirements = ["types-aiofiles", "aiofiles", "aiohttp", "requests", "types-requests"]

setup(
    name="phantombrowser",
    version="v0.0.2",
    description="Typed Python wrapper for Phantomjs Cloud API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="guangrei",
    author_email="myawn@pm.me",
    url="https://github.com/guangrei/PhantomBrowser",
    packages=["PhantomBrowser"],
    package_data={"PhantomBrowser": ["py.typed"]},
    license="MIT",
    platforms="any",
    install_requires=requirements,
)
