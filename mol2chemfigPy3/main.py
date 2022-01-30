# -*- coding: utf-8 -*-
# Author: Nianze A. TAO (Omozawa SUENO)
"""
package main
"""
import sys
from .processor import process


def main() -> None:
    """
    console function

    :return: None
    """
    success, result = process(raw_args=sys.argv[1:], program_name=sys.argv[0])
    if success:
        print(result.render_user())
    else:
        print(result)


if __name__ == "__main__":
    main()
