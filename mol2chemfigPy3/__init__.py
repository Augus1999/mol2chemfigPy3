# -*- coding: utf-8 -*-
# make this a python package
"""
a python 3 version of mol2chemfig.
mol2chemfig generates chemfig code from molfiles.
"""
from .processor import process
from .common import program_version
from .addin import mol2chemfig
__version__ = program_version
__Author__ = 'Nianze A. TAO'
__all__ = ['process', 'mol2chemfig', '__version__']
