# -*- coding: utf-8 -*-
# make this a python package
"""
a python 3 version of mol2chemfig.
mol2chemfig generates chemfig code from mol files.
"""
import re
from typing import Optional
from .main import main
from .processor import process
from .common import program_version

__version__ = program_version
__Author__ = "Nianze A. TAO"
__all__ = ["main", "mol2chemfig", "__version__"]


def mol2chemfig(
    content: str,
    *args: str,
    rotate: float = 0.0,
    aromatic: bool = True,
    marker: Optional[str] = None,
    name: Optional[str] = None,
    relative_angle: bool = False,
    show_carbon: bool = False,
    show_methyl: bool = False,
    inline: bool = False,
) -> Optional[str]:
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
    others = " ".join(args)
    arg = (
        f'-wz{"o" if aromatic else ""}{"v" if relative_angle else ""}'
        f'{"c" if show_carbon else ""}{"m" if show_methyl else ""}'
        f' -a {rotate} {"" if marker is None else "-g "+marker}'
        f' {"" if name is None else "-l "+name} {others}'
    )
    arg = re.sub(r"\s+", " ", arg).split()
    if content.endswith(
        (
            ".mol",
            ".smi",
        )
    ):
        arg += ["-i", "file", content]
    else:
        try:
            pubchem_id = int(content)
            arg += ["-i", "pubchem", str(pubchem_id)]
        except ValueError:
            arg += ["-i", "direct", content]
    success, result = process(raw_args=arg, inline=True)
    if inline:
        return result.render_user() if success else result
    print(f'{result.render_user() if success else "Failed..."}')
