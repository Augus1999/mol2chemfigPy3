# -*- coding: utf-8 -*-
# Author: Nianze A. TAO (Omozawa SUENO)
"""
package main
"""
import sys

try:
    from pip._vendor import colorama

    colour = True
except ImportError:
    colour = False
from .processor import process


def main(program_name: str = sys.argv[0]) -> None:
    """
    console function

    :param program_name: program name
    :return: None
    """
    if colour:
        colorama.init()
    success, result = process(raw_args=sys.argv[1:], program_name=program_name)
    if success:
        print(result.render_user())
    else:
        print(result)
    if colour:
        colorama.deinit()
