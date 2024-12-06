# -*- coding: utf-8 -*-

# Learn more: https://github.com/NeurosystemsCo/manychrome/setup.py

from setuptools import setup

with open("README.rst") as f:
    readme = f.read()

with open("LICENSE") as f:
    license = f.read()

setup(
    name="manychrome",
    version="0.1.0",
    description="A simple package to colour and style your text printed on the CLI.",
    long_description=readme,
    url = "https://github.com/NeurosystemsCo/manychrome",
    license=license,
    author="Maria Wenner",
    author_email="mail@neurosystems.co",
    packages=['manychrome'],
    classifiers=[
    "Programming Language :: Python :: 3",
    "Operating System :: MacOS"
    ],
    python_requires='>=3.8',
)
