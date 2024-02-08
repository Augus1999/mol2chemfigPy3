from mol2chemfigPy3 import mol2chemfig


def test():
    target = r"""\chemfig{H-[:330,0.62]-[:30](-[:90]O-[:30,0.62]H)(%
-[:270,,,,draw=none]\mcfcringle{1.3})-[:330](-[:30,0.62]H)-[:270](%
-[:330,0.62]H)-[:210](-[:270,0.62]H)-[:150](-[:90])-[:210,0.62]H}"""
    assert mol2chemfig("996", inline=True) == target
