# -*- coding: utf-8 -*-
# Author: Nianze A. TAO (Omozawa SUENO)
"""
package main
"""
import sys
import colorama
from .processor import process


def main(program_name: str = sys.argv[0]) -> None:
    """
    console function

    :param program_name: program name
    :return: None
    """
    colorama.just_fix_windows_console()
    success, result = process(raw_args=sys.argv[1:], program_name=program_name)
    if success:
        print(result.render_user())
    else:
        print(result)
    colorama.deinit()
