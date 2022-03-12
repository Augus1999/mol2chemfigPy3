# -*- coding: utf-8 -*-
# Author: Nianze A. TAO (Omozawa SUENO)
import os
import re
from pathlib import Path
from shutil import rmtree
from setuptools import setup, find_packages

init_file = Path("mol2chemfigPy3") / "common.py"

with open(init_file, mode="r", encoding="utf-8") as f:
    lines = f.readlines()
    for line in lines:
        if "program_version" in line:
            version = re.findall(r"[0-9]+\.[0-9]+\.[0-9]+", line)
            if len(version) != 0:
                version = version[0]
                print("version:", version)
                break

with open("README.md", mode="r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mol2chemfigPy3",
    version=version,
    url="https://augus1999.github.io/mol2chemfigPy3/",
    description="python3 version of mol2chemfig",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT licence",
    package_dir={"mol2chemfigPy3": "mol2chemfigPy3"},
    author="Nianze A. Tao",
    author_email="TaoN@cardiff.ac.uk",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=["epam.indigo"],
    project_urls={"Source": "https://github.com/Augus1999/mol2chemfigPy3"},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Chemistry",
    ],
    keywords=["Chemistry", "chemfig"],
    entry_points={"console_scripts": ["mol2chemfig=mol2chemfigPy3.main:main"]},
)

if os.path.exists("build"):
    rmtree("build")
if os.path.exists("mol2chemfigPy3.egg-info"):
    rmtree("mol2chemfigPy3.egg-info")
