# -*- coding: utf-8 -*-
# Author: Nianze A. TAO (Omozawa SUENO)
"""
package main
"""
import sys
import platform
from .processor import process

_system = platform.system()


def main(program_name: str = sys.argv[0]) -> None:
    """
    console function

    :param program_name: program name
    :return: None
    """
    if _system == "Windows":
        import colorama

        if hasattr(colorama, "just_fix_windows_console"):
            colorama.just_fix_windows_console()
        elif hasattr(colorama, "init"):
            colorama.init()
    success, result = process(raw_args=sys.argv[1:], program_name=program_name)
    if success:
        print(result.render_user())
    else:
        print(result)
    if _system == "Windows":
        colorama.deinit()
