# -*- coding: utf-8 -*-
# Author: Nianze A. TAO (Omozawa SUENO)
"""
Reaction SMILES --> chemfig code.
"""
import sys
import textwrap
from mol2chemfigPy3 import mol2chemfig


def rxn2chemfig(rxn: str, ignore_structure_check: bool = False) -> str:
    reactants, products = rxn.split(">>")
    reactants = reactants.split(".")
    products = products.split(".")
    reactant_chemfig = [
        mol2chemfig(i, f"{'-r' if ignore_structure_check else ''}", inline=True)
        for i in reactants
    ]
    product_chemfig = [
        mol2chemfig(i, f"{'-r' if ignore_structure_check else ''}", inline=True)
        for i in products
    ]
    reactant_block = "\n\\+\n".join(reactant_chemfig)
    product_block = "\n\\+\n".join(product_chemfig)
    rxn_chemfig = (
        r"\schemestart"
        f"\n{textwrap.indent(reactant_block, '  ')}\n"
        f"{textwrap.indent(r'\arrow', '  ')}"
        f"\n{textwrap.indent(product_block, '  ')}\n"
        r"\schemestop"
    )
    return rxn_chemfig


if __name__ == "__main__":
    print(rxn2chemfig(sys.argv[1], sys.argv[2:]))
