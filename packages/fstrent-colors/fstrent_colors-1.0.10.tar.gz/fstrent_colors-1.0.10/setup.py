# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name="fstrent_colors",
    version="1.0.10",
    packages=find_packages(),
    install_requires=[
        "colorama",
    ],
    author="FSTrent",
    author_email="wrmartel3@gmail.com",
    description="Enhanced colors options for terminal output",
    long_description=open("README.md", encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/wrm3/fstrent_colors",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
) 