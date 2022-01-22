# -*- coding: utf-8 -*-
# author: Nianze A. TAO (Omozawa SUENO)
"""
mol2chemfigPy3 inline add-in
"""
import os
import re
from typing import Optional
from .processor import process


def mol2chemfig(content: str,
                rotate: float = 0.0,
                aromatic: bool = True,
                marker: Optional[str] = None,
                name: Optional[str] = None,
                relative_angle: bool = False,
                show_carbon: bool = False,
                show_methyl: bool = False,
                inline: bool = False,
                *args: str) -> Optional[str]:
    """
    wrapper of mol2chemfigPy3.process(.)

    :param content: chemical file name, InChem, SMILES, or Pubchem index
    :param rotate: rotation angle
    :param aromatic: whether drawing circle(s) in aromatic ring(s)
    :param marker: mark atoms, e.g., with value 'a', atom 2 will be labeled @{a2}
    :param name: name of the molecule
    :param relative_angle: whether using relative bond angles
    :param show_carbon: whether show carbon symbol
    :param show_methyl: whether show methyl symbol
    :param inline: inline mode: if true return the result else print the result
    :return: None or result
    """
    assert isinstance(aromatic, bool), "This value should be in type Bool"
    assert isinstance(relative_angle, bool), "This value should be in type Bool"
    assert isinstance(show_carbon, bool), "This value should be in type Bool"
    assert isinstance(show_methyl, bool), "This value should be in type Bool"
    a = {True: 'o', False: ''}
    v = {True: 'v', False: ''}
    c = {True: 'c', False: ''}
    m = {True: 'm', False: ''}
    _g = {True: '', False: f'-g {marker}'}
    _l = {True: '', False: f'-l {name}'}
    g = _g[marker is None]
    l = _l[name is None]
    others = ' '.join(args)
    arg = f'-wz{a[aromatic] + v[relative_angle] + c[show_carbon] + m[show_methyl]}' \
          f' -a {rotate} {g} {l} {others}'
    arg = re.sub(r'\s+', ' ', arg)
    if os.path.isfile(content):
        arg += f' -i file \"{content}\"'
    else:
        if re.match(r'[0-9]+', content).group(0) == content:
            arg += f' -i pubchem {content}'
        else:
            arg += f' -i direct {content}'
    success, result = process(raw_args=arg)
    if success:
        if inline:
            return result.render_user()
        print(result.render_user())
    else:
        if inline:
            return result
        print("Failed...")
