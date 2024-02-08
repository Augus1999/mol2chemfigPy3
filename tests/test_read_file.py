from pathlib import Path
from mol2chemfigPy3 import mol2chemfig


cwd = Path(__file__).parent

def test():
    target = r"""\chemfig{@{a7}HO-[@{a4-7},,2]@{a4}-[@{a3-4}:300]@{a3}-[@{a2-3}]@{a2}%
-[@{a1-2}:60]@{a1}(-[:180,,,,draw=none]\mcfcringle{1.3})-[@{a1-6}:120]@{a6}%
-[@{a5-6}:180]@{a5}(-[@{a4-5}:240])}"""
    assert mol2chemfig(cwd / "phenol.smi", "-p", marker="a", inline=True) == target
