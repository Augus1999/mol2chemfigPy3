# -*- coding: utf-8 -*-
# author: Nianze A. TAO
import os
from .processor import process


def mol2chemfig(c: str,
                rotate: float = 0.0,
                aromatic: bool = True) -> None:
    """
    wrapper of mol2chemfigPy3.process(.)

    :param c: chemical file name, InChem, SMILES, or Pubchem index
    :param rotate: rotation angle
    :param aromatic: whether draw circle(s) in aromatic ring(s)
    :return: None
    """
    a = {True: 'o', False: ''}
    if os.path.isfile(c):
        arg = f'-wz{a[aromatic]} -a {rotate} -i file {c}'
    else:
        try:
            int(c)
            arg = f'-wz{a[aromatic]} -a {rotate} -i pubchem {c}'
        except ValueError:
            arg = f'-wz{a[aromatic]} -a {rotate} -i direct {c}'
    success, result = process(raw_args=arg)
    if success:
        print(result.render_user())
    else:
        print("Failed...")
