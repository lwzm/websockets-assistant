#!/usr/bin/env python

from setuptools import setup

name = "websockets-assistant"
author = "lwzm"

with open("README.md") as f:
    long_description = f.read()


setup(
    name=name,
    version="2.2",
    description="Util for create websocket client(s) quickly",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=author,
    author_email="{}@qq.com".format(author),
    keywords="websockets websocket util ws wss".split(),
    url="https://github.com/{}/{}".format(author, name),
    py_modules=["websockets_assistant"],
    install_requires="websockets".split(),
    classifiers=[
        "Environment :: Console",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
    ],
)
