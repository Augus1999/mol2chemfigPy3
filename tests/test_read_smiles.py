from mol2chemfigPy3 import mol2chemfig


def test():
    target = r"""\chemfig{-[:138]N-[:84](-[:210,0.85,,,draw=none]\mcfcringle{1.03})-[:156]N%
-[:228]-[:300](-[:12]\phantom{N})-[:240](=[:300]O)-[:180]N(-[:240])-[:120](%
=[:180]O)-[:60]N(-)-[:120]}"""
    assert mol2chemfig("CN1C=NC2=C1C(=O)N(C(=O)N2C)C", "-p", inline=True) == target

    target = r"""\chemfig{CH_3-[:108,,1]N-[:54](-[:180,0.85,,,draw=none]\mcfcringle{1.03})%
-[:126]N-[:198]-[:270](-[:342]\phantom{N})-[:210](=[:270]O)-[:150]N(%
-[:210,,,2]H_3C)-[:90](=[:150]O)-[:30]N(-[:330])-[:90,,,1]CH_3}"""
    assert mol2chemfig("CN1C=NC2=C1C(=O)N(C(=O)N2C)C", "-p", rotate=-30, show_methyl=True, inline=True) == target
