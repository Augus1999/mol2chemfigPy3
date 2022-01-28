# -*- coding: utf-8 -*-
# Author: Nianze A. TAO (Omozawa SUENO)
import os
from shutil import rmtree
from setuptools import setup, find_packages
from mol2chemfigPy3 import __version__


with open("README.md", mode="r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='mol2chemfigPy3',
    version=__version__,
    url='https://augus1999.github.io/mol2chemfigPy3/',
    description='python3 version of mol2chemfig',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT licence',
    package_dir={'mol2chemfigPy3': 'mol2chemfigPy3'},
    author='Nianze A. Tao',
    author_email='TaoN@cardiff.ac.uk',
    scripts=['mol2chemfig', 'mol2chemfig.py'],
    packages=find_packages(),
    python_requires='>=3.7',
    install_requires=['epam.indigo'],
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
)

if os.path.exists('build'):
    rmtree('build')
if os.path.exists('mol2chemfigPy3.egg-info'):
    rmtree('mol2chemfigPy3.egg-info')
