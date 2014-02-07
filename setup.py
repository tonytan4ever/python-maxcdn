#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name="maxcdn",
    version="0.0.1",
    description="A Python REST Client for MaxCDN REST Web Services",
    author="Joshua P. Mervine",
    author_email = "joshua@mervine.net",
    license = "MIT",
    keywords = "MAxCDN CDN API REST",
    packages=['maxcdn'],
    include_package_data=True,
    install_requires=[
      'requests',
      'requests_oauthlib',
      'certifi'
    ],
    url='http://www.maxcdn.com',
)
