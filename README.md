# mol2chemfigPy3

This is NOT an official version of mol2chemfig for python 3.

There are always too few free tools for chemistry, while mol2chemfig is a good one of them. But it was written in python2. Nowadays who are still using py2? LOL

Simply applying 2to3 to it does't work, alas.

mol2chemfigPy3 is a simple translation from py2 to py3 based on old mol2chemfig version 1.4 (well, 27/03/2014, more than 7 years ago🤐[mol2chemfig (uwaterloo.ca)](http://chimpsky.uwaterloo.ca/mol2chemfig/download)), and it, of course, has bugs.

## Install

* first install indigo

  ```bash
  $ pip install epam.indigo
  ```

* then run

  ```bash
  $ python setup.py bdist_wheel
  $ python setup.py install
  ```

## Usage

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

## Document

See official document [mol2chemfig-doc.pdf (uwaterloo.ca)](http://chimpsky.uwaterloo.ca/m2cf_static/mol2chemfig-doc.pdf)

## Known issue(s)

* run arguments containing ` pubchem` will output errors
* direct using output file from mol2chemfig doesn't work. Copy the content to your own LaTax files

## Licence

MIT licence