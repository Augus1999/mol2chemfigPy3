from mol2chemfigPy3 import mol2chemfig


def test():
    target = r"""\chemfig{H-[:210,0.62]-[:150](-[:90]O-[:30,0.62]H)(%
-[:270,,,,draw=none]\mcfcringle{1.3})-[:210](-[:150,0.62]H)-[:270](%
-[:210,0.62]H)-[:330](-[:270,0.62]H)-[:30](-[:90])-[:330,0.62]H}"""
    assert mol2chemfig("996", inline=True) == target
