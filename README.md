# mol2chemfigPy3

[![PyPI](https://img.shields.io/pypi/v/mol2chemfigPy3?color=ff69b4)](https://pypi.org/project/mol2chemfigPy3/)
[![Downloads](https://static.pepy.tech/personalized-badge/mol2chemfigpy3?period=total&units=international_system&left_color=black&right_color=green&left_text=Downloads)](https://pepy.tech/project/mol2chemfigpy3)
![OS](https://img.shields.io/badge/OS-Win%20|%20Linux%20|%20macOS-blue?color=00B16A)
![python](https://img.shields.io/badge/Python-3.8%20|%203.9%20|%203.10-blue.svg?color=dd9b65)
![black](https://img.shields.io/badge/code%20style-black-black)

This is NOT an official version of mol2chemfig for python 3.

mol2chemfigPy3 is a translation from py2 to py3 based on
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

## Document

See official document [mol2chemfig-doc.pdf (uwaterloo.ca)](http://chimpsky.uwaterloo.ca/m2cf_static/mol2chemfig-doc.pdf)

## License

MIT license

