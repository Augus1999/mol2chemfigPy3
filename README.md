# mol2chemfigPy3

Current version 1.5.2 (transferred from mol2chemfig v1.5).

This is NOT an official version of mol2chemfig for python 3.

There are always too few free tools for chemistry, while mol2chemfig is a good one of them. But it was written in
python2. Nowadays, who are still using py2? LOL

Simply applying 2to3 to it doesn't work, alas.

mol2chemfigPy3 is a simple translation from py2 to py3 based on old mol2chemfig version 1.5 (the python codes are the
same as 1.4🤔 [mol2chemfig (uwaterloo.ca)](http://chimpsky.uwaterloo.ca/mol2chemfig/download)).

## Install

### build from source

this requires `setuptools` and `wheel` installed

* first `cd` to where `setup.py` locates

  ```bash
  $ cd <path>
  ```

* then run

  ```bash
  $ pip install .
  ```

If you prefer installing from wheel, you can download [here](https://github.com/Augus1999/mol2chemfigPy3/releases).

### install from PyPi

[![Downloads](https://static.pepy.tech/personalized-badge/mol2chemfigpy3?period=total&units=international_system&left_color=black&right_color=green&left_text=Downloads)](https://pepy.tech/project/mol2chemfigpy3)

```bash
$ pip install -U mol2chemfigPy3
```

## Usage

### Use in command line

> Attention: to render the colours on Windows platform, run it in modern terminals, e.g. ___Windows Terminal___.

Run, for example:

```bash
$ mol2chemfig -zw -i direct "C1=CC=C(C=C1)O"
```

it will give you `\chemfig{OH-[:180,,1]=_[:240]-[:180]=_[:120]-[:60]=_(-[:300])}`

Run, for another example:

```bash
$ mol2chemfig -zw -i direct "C1=CC=C(C=C1)O" > phenol-smi-terse.tex
```

it will write result to file `phenol-smi-terse.tex`

Run, for again another example:

```bash
$ mol2chemfig -zw -i pubchem 99
```

it will give you

```latex
\chemfig{O=[:137.9]P(-[:47.9]O-[:107.9,0.62]H)(-[:137.9]O-[:197.9,0.62]H)%
-[:227.9]O-[:287.9](-[:44.9,0.62]H)-[:233.9](-[:179.9]O-[:119.9,0.62]H)(%
-[:116.9,0.62]H)-[:305.9](-[:251.9]N-[:197.8,0.994]=^[:150]N-[:210](%
-[:150,0.62]H)=^[:270]N-[:330](=^[:30](-[:90])-[:342.1,0.994]N%
=^[:54.1,0.994](-[,0.62]H)-[:126,0.994]\phantom{N})-[:270]N(-[:330,0.62]H)%
-[:210,0.62]H)(-[:314.9,0.62]H)-[:17.9]O-[:89.9](-[:161.9])(-[:332.9,0.62]H%
)-[:35.9](-[:55.9,0.62]H)(-[:135.9,0.62]H)-[:335.9]O-[:35.9]P(-[:305.9]O%
-[:245.9,0.62]H)(=[:125.9]O)-[:35.9]O-[:335.9]P(-[:65.9]O-[:125.9,0.62]H)(%
=[:245.9]O)-[:335.9]O-[:35.9](-[:55.9,0.62]H)(-[:135.9,0.62]H)-[:335.9](%
-[:65.9](-[:65.9,0.62]H)(-[:155.9,0.62]H)-[:335.9,0.62]H)(-[:245.9](%
-[:245.9,0.62]H)(-[:335.9,0.62]H)-[:155.9,0.62]H)-[:335.9](-[:275.9]O%
-[:335.9,0.62]H)(-[:215.9,0.62]H)-[:35.9](=[:95.9]O)-[:335.9]N(%
-[:275.9,0.62]H)-[:35.9](-[:55.9,0.62]H)(-[:135.9,0.62]H)-[:335.9](%
-[:235.9,0.62]H)(-[:315.9,0.62]H)-[:35.9](=[:95.9]O)-[:335.9]N(%
-[:275.9,0.62]H)-[:35.9](-[:55.9,0.62]H)(-[:135.9,0.62]H)-[:335.9](%
-[:235.9,0.62]H)(-[:315.9,0.62]H)-[:35.9]S-[:335.9](=[:275.9]O)-[:35.9](%
-[:95.9,0.62]H)=[:335.9](-[:35.9](-[:35.9,0.62]H)(-[:125.9,0.62]H)%
-[:305.9,0.62]H)-[:275.9](-[:185.9,0.62]H)(-[:275.9,0.62]H)-[:5.9,0.62]H}
```

(it's [Coenzyme A, S-(3-methyl-2-butenoate)](https://pubchem.ncbi.nlm.nih.gov/compound/99#section=Synonyms) by the way
😜)

### Use as a python package (new add in to this python 3 version)

This is not included in the old Py2 version of mol2chemfig.

> mol2chemfigPy3.___mol2chemfig___(content: _str_, *args: _str_, rotate: _float = 0.0_, aromatic: _bool = True_, marker: _Optional[str] = None_, name: _Optional[str] = None_, relative_angle: _bool = False_, show_carbon: _bool = False_, show_methyl: _bool = False_, inline: _bool = False_)

e. g.

```python
from mol2chemfigPy3 import mol2chemfig

mol2chemfig('996')  # search the PubChem database

mol2chemfig('C1=CC=C(C=C1)O')  # transfer InChI/SMILES to chemfig

mol2chemfig('.\methanol.smi')  # from a file
```

## Document

See official document [mol2chemfig-doc.pdf (uwaterloo.ca)](http://chimpsky.uwaterloo.ca/m2cf_static/mol2chemfig-doc.pdf)

## License

MIT license

