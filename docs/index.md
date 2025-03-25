`mol2chemfigPy3` is a translation from py2 to py3 based on
old [mol2chemfig](http://chimpsky.uwaterloo.ca/mol2chemfig/download) version 1.5.

## Install

### install from PyPi

```bash
$ pip install -U mol2chemfigPy3
```

## Usage

### Use in command line

> `mol2chemfig` and `python -m mol2chemfigPy3` are equivalent.

#### 1. getting version

```bash
$ mol2chemfig --version
```

#### 2. getting help

```bash
$ mol2chemfig -h
```

#### 3. some examples

##### 3.1 converting SMILES

```bash
$ mol2chemfig -zw -i direct "C1=CC=C(C=C1)O"
```

it will give you 

```latex
\chemfig{OH-[:180,,1]=_[:240]-[:180]=_[:120]-[:60]=_(-[:300])}
```

##### 3.2 writing to an output file

```bash
$ mol2chemfig -zw -i direct "C1=CC=C(C=C1)O" > phenol-smi-terse.tex
```

it will write result to file `phenol-smi-terse.tex`

##### 3.3 searching PubChem database

```bash
$ mol2chemfig -zw -i pubchem 996
```

##### 3.4 reading from a file

```bash
$ mol2chemfig -zw peniciling.mol
```

### Use as a python package (new add in to this python 3 version)

This is not included in the original Py2 version of mol2chemfig.

> mol2chemfigPy3.___mol2chemfig___(content: _str_, *args: _str_, rotate: _float = 0.0_, aromatic: _bool = True_, marker: _Optional[str] = None_, name: _Optional[str] = None_, relative_angle: _bool = False_, show_carbon: _bool = False_, show_methyl: _bool = False_, inline: _bool = False_)

e. g.

```python
from mol2chemfigPy3 import mol2chemfig

mol2chemfig('996')  # search the PubChem database

mol2chemfig('C1=CC=C(C=C1)O')  # transfer InChI/SMILES to chemfig

mol2chemfig('./methanol.smi')  # from a file
```

## To future maintainers

The static callgraph of this project is:

[![callgraph](image/callgraph.svg)](image/callgraph.svg)

## Document

~~See official document [mol2chemfig-doc.pdf (uwaterloo.ca)](http://chimpsky.uwaterloo.ca/m2cf_static/mol2chemfig-doc.pdf)~~

The website seems down, so here is a mirror [mol2chemfig Documentation Version 1.5](https://mirror.ox.ac.uk/sites/ctan.org/graphics/mol2chemfig/mol2chemfig-doc.pdf). 

## License

MIT license

## We stand with Ukraine

[![Stand With Ukraine](https://raw.githubusercontent.com/vshymanskyy/StandWithUkraine/main/banner2-direct.svg)](https://stand-with-ukraine.pp.ua)
