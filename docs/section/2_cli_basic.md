> Note that `mol2chemfig` and `python -m mol2chemfigPy3` are equivalent.

### 1. getting version

```bash
$ mol2chemfig --version
```

### 2. getting help

```bash
$ mol2chemfig -h
```

### 3. converting

#### 3.1 converting SMILES

```bash
$ mol2chemfig -zw -i direct "C1=CC=C(C=C1)O"
```

which will give you 

```latex
\chemfig{OH-[:180,,1]=_[:240]-[:180]=_[:120]-[:60]=_(-[:300])}
```

Sometimes, `epam.indigo` cannot correctly parse some aromatic compound that raises an error of 'incorrect structure', even though the molecular structure is correct. Or from time to time we want to draw molecules with uncommon valencies. In these cases, using flag `-r` can bypass the structural checking mechanism of `epam.indigo`.

For example,

```bash
$ mol2chemfig -zw -r -i direct "c1ccncc1"
```

#### 3.2 writing to an output file

```bash
$ mol2chemfig -zw -i direct "C1=CC=C(C=C1)O" > phenol-smi-terse.tex
```

which will write result to file `phenol-smi-terse.tex`

#### 3.3 searching PubChem database

```bash
$ mol2chemfig -zw -i pubchem 996
```

#### 3.4 reading from a file

```bash
$ mol2chemfig -zw peniciling.mol
```