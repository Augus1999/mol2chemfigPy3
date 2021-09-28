# mol2chemfigPy3

Current version 1.4.1 (transferred from mol2chemfig v1.4).

This is NOT an official version of mol2chemfig for python 3.

There are always too few free tools for chemistry, while mol2chemfig is a good one of them. But it was written in python2. Nowadays who are still using py2? LOL

Simply applying 2to3 to it doesn't work, alas.

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

### Use in command line

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

(it's [Coenzyme A, S-(3-methyl-2-butenoate)](https://pubchem.ncbi.nlm.nih.gov/compound/99#section=Synonyms) by the way 😜)

### Use as a python package (new add in to this python 3 version)

This is not included in the old Py2 version of mol2chemfig.

e. g. 

```python
from mol2chemfigPy3 import mol2chemfig


mol2chemfig('996')  # search the PubChem database

mol2chemfig('C1=CC=C(C=C1)O')  # transfer InChI to chemfig

mol2chemfig('.\methanol.smi')  # from a file
```



## Document

See official document [mol2chemfig-doc.pdf (uwaterloo.ca)](http://chimpsky.uwaterloo.ca/m2cf_static/mol2chemfig-doc.pdf)

## Known issue(s)

* direct using output file from mol2chemfig doesn't work. Copy the content to your own LaTaX files

## License

MIT license