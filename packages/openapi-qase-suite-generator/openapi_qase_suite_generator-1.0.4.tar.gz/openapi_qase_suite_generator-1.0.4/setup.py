#!/usr/bin/env python3

from setuptools import setup, find_packages
import os


def get_version():
    import os
    # Try to get version from environment variable
    version = os.environ.get('PACKAGE_VERSION', '0.0.0')
    return version


setup(
    version=get_version(),
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)
