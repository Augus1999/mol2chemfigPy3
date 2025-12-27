import os
from pathlib import Path
import pytest
from mol2chemfigPy3 import mol2chemfig


cwd = Path(__file__).parent

target1 = r"""\chemfig{@{a7}HO-[@{a4-7},,2]@{a4}-[@{a3-4}:300]@{a3}-[@{a2-3}]@{a2}%
-[@{a1-2}:60]@{a1}(-[:180,,,,draw=none]\mcfcringle{1.3})-[@{a1-6}:120]@{a6}%
-[@{a5-6}:180]@{a5}(-[@{a4-5}:240])}"""
target2 = r"""\chemfig{-[:180](-[:300,,,,draw=none]\mcfcringle{1.3})-[:240]-[:300]N-%
-[:60](-[:120])}"""
target3 = r"""\chemfig{@{a1}^{\mcfplus}H_3N-[@{a1-2}:6,,3]@{a2}-[@{a2-3}:306]@{a3}%
-[@{a3-4}:6]@{a4}-[@{a4-5}:60]@{a5}(%
-[:294,0.85,,,draw=none]\mcfcringle{1.03})-[@{a5-6}:348]@{a6}%
-[@{a6-7}:276,,,1]@{a7}NH-[@{a7-8}:204,,1]@{a8}(-[@{a4-8}:132])}"""


@pytest.mark.parametrize(
    "input_value,arg,marker_,expected",
    [
        ("C1=CC=C(C=C1)O", "-p", "a", target1),
        ("c1ccncc1", "-r", None, target2),
        ("[NH3+]CCc1cc[nH]c1", "-q", "a", target3),
    ],
)
def test(input_value, arg, marker_, expected):
    with open(cwd / "mol.smi", "w") as f:
        f.write(input_value)
    assert mol2chemfig(cwd / "mol.smi", arg, marker=marker_, inline=True) == expected
    os.remove(cwd / "mol.smi")
