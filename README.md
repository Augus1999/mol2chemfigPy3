# mol2chemfigPy3

[![PyPI](https://img.shields.io/pypi/v/mol2chemfigPy3?color=ff69b4)](https://pypi.org/project/mol2chemfigPy3/)
[![CI_tox](https://github.com/nbehrnd/mol2chemfigPy3/actions/workflows/tox.yml/badge.svg)](https://github.com/nbehrnd/mol2chemfigPy3/actions/workflows/tox.yml)
![black](https://img.shields.io/badge/code%20style-black-black)
[![Stand With Ukraine](https://raw.githubusercontent.com/vshymanskyy/StandWithUkraine/main/badges/StandWithUkraine.svg)](https://stand-with-ukraine.pp.ua)

This is NOT an official version of mol2chemfig for python 3.

`mol2chemfigPy3` is a translation from py2 to py3 based on
old [mol2chemfig](http://chimpsky.uwaterloo.ca/mol2chemfig/download) version 1.5.

## Install

### install from PyPi

```bash
$ pip install -U mol2chemfigPy3
```

### install with a copy of this forked (downstream) repository

This repository is a downstream fork relative to blessed repository
currently archived by Augus1999.  Organized around a `pyproject.toml`
file, runtime dependencies are declared in way that you may either
use `build` as installed by `pip`, or `uv build` to obtain a .whl

```bash
python -m build .
uv build .
````

in the local `dist/` folder.  The .whl then can be used as usual as
a local reference (instead of PyPI).  Note that dependencies still
are resolved from pypi.org, especially if you want to develop the
module further, e.g.

```bash
pip install -e .[dev]
```

to collect for instance pytest.

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

> mol2chemfigPy3.___mol2chemfig___(content: _Union[str, int, pathlib.Path]_, *args: _str_, rotate: _float = 0.0_, aromatic: _bool = True_, marker: _Optional[str] = None_, name: _Optional[str] = None_, relative_angle: _bool = False_, show_carbon: _bool = False_, show_methyl: _bool = False_, inline: _bool = False_) &#8594; _Optional[str]_

e. g.

```python
from mol2chemfigPy3 import mol2chemfig

mol2chemfig('996')  # search the PubChem database

mol2chemfig('C1=CC=C(C=C1)O')  # transfer InChI/SMILES to chemfig

mol2chemfig('./methanol.smi')  # from a file
```

## Document

~~See official document [mol2chemfig-doc.pdf (uwaterloo.ca)](http://chimpsky.uwaterloo.ca/m2cf_static/mol2chemfig-doc.pdf)~~

The website seems down, so here is a mirror [mol2chemfig Documentation Version 1.5](https://mirror.ox.ac.uk/sites/ctan.org/graphics/mol2chemfig/mol2chemfig-doc.pdf)

## License

MIT license
