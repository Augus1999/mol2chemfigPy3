This is not included in the original mol2chemfig.

> mol2chemfigPy3.___mol2chemfig___(content: _str_, *args: _str_, rotate: _float = 0.0_, aromatic: _bool = True_, marker: _Optional[str] = None_, name: _Optional[str] = None_, relative_angle: _bool = False_, show_carbon: _bool = False_, show_methyl: _bool = False_, inline: _bool = False_) &#8594; str | None

&nbsp;&nbsp;&nbsp; A wrapper of `~mol2chemfigPy3.process(...)` function.

&nbsp;&nbsp;&nbsp; Note that this function uses file extensions to judge whether an input is a valid file name or not. Please make sure your file names end with `.gz .sdf .rdf .mol .rxn .txt .cml .mrv .xml .smi`.

> > Parameters
> >
> > * __content__ - chemical file name, InChI, SMILES, or PubChem index
> > * __rotate__ - rotation angle
> > * __aromatic__ - whether to draw circle(s) in aromatic ring(s)
> > * __marker__ - mark atoms, e.g., with value 'a', atom 2 will be labeled as @{a2}
> > * __name__ - name of the molecule
> > * __relative\_angle__ - whether to use relative bond angles
> > * __show\_carbon__ - whether to show carbon symbols
> > * __show\_methyl__ - whether to show methyl symbols
> > * __inline__ - inline mode: if `True` return the result else print the result

### 1. basic usage

```python
from mol2chemfigPy3 import mol2chemfig

mol2chemfig('996')  # search the PubChem database

mol2chemfig('C1=CC=C(C=C1)O')  # transfer InChI/SMILES to chemfig

mol2chemfig('./methanol.smi')  # read from a file
```

### 2. bypassing the structure check

```python
mol2chemfig('c1ccncc1', '-r')
```

### 3. parsing reactions

Some users suggested that we should include support for reaction SMILES. For some reasons, it is not flexible to add this feature in the package. However, it is easy to write a function to handle reaction via API, e.g.,

```python
import textwrap

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
```

which defines a template to translate reactants and products to `chemfig` code.
