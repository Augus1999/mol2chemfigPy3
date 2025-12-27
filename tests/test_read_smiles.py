import pytest
from mol2chemfigPy3 import mol2chemfig

target1 = r"""\chemfig{-[:138]N-[:84](-[:210,0.85,,,draw=none]\mcfcringle{1.03})-[:156]N%
-[:228]-[:300](-[:12]\phantom{N})-[:240](=[:300]O)-[:180]N(-[:240])-[:120](%
=[:180]O)-[:60]N(-)-[:120]}"""
target2 = r"""\chemfig{CH_3-[:108,,1]N-[:54](-[:180,0.85,,,draw=none]\mcfcringle{1.03})%
-[:126]N-[:198]-[:270](-[:342]\phantom{N})-[:210](=[:270]O)-[:150]N(%
-[:210,,,2]H_3C)-[:90](=[:150]O)-[:30]N(-[:330])-[:90,,,1]CH_3}"""


@pytest.mark.parametrize(
    "input_value,arg,rotate_,show_methyl_,expected",
    [
        ("CN1C=NC2=C1C(=O)N(C(=O)N2C)C", "-p", 0, False, target1),
        ("CN1C=NC2=C1C(=O)N(C(=O)N2C)C", "-p", -30, True, target2),
    ],
)
def test(input_value, arg, rotate_, show_methyl_, expected):
    assert (
        mol2chemfig(
            input_value, arg, rotate=rotate_, show_methyl=show_methyl_, inline=True
        )
        == expected
    )
