# -*- coding: utf-8 -*-
# make this a python package
from .processor import process
from .common import program_version
from .addin import mol2chemfig
__version__ = program_version
__all__ = ['process', 'mol2chemfig', '__version__']
