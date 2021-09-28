# -*- coding: utf-8 -*-
import os
from .processor import process


def mol2chemfig(c: str, rotate: float = 0.0, aromatic: bool = True) -> None:
    a = {True: 'o', False: ''}
    if os.path.isfile(c):
        arg = f'-wz{a[aromatic]} -a {rotate} -i file {c}'
        success, result = process(rawargs=arg)
        if success:
            print(result.render_user())
        else:
            print('Failed')
    else:
        try:
            int(c)
            arg = f'-wz{a[aromatic]} -a {rotate} -i pubchem {c}'
        except ValueError:
            arg = f'-wz{a[aromatic]} -a {rotate} -i direct {c}'
        success, result = process(rawargs=arg)
        if success:
            print(result.render_user())
        else:
            print('Failed')
