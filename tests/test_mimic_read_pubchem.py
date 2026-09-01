import platform
from pathlib import Path
import pytest
from mol2chemfigPy3 import mol2chemfig, processor


_sys = platform.system()
FIXTURE_DIR = Path(__file__).parent / "data_pubchem"

target1 = r"""\chemfig{H-[:210,0.62]-[:150](-[:90]O-[:30,0.62]H)(%
-[:270,,,,draw=none]\mcfcringle{1.3})-[:210](-[:150,0.62]H)-[:270](%
-[:210,0.62]H)-[:330](-[:270,0.62]H)-[:30](-[:90])-[:330,0.62]H}"""
target2 = r"""\chemfig{H-[:300]-(-[:60]H)(-[:240,,,,draw=none]\mcfcringle{1.3})-[:300](-H%
)-[:240](-[:300]H)-[:180](-[:240]H)-[:120](-[:60])-[:180]H}"""
target3 = r"""\chemfig{O=[:300](-[:240]O-[:180]H)-(-[:322.5]H)(-[:277.5]H)-[:60]S-H}"""
target4 = r"""\chemfig{@{sym3}O=[@{sym3-5}:90,1.613]@{sym5}(%
-[@{sym2-5}::60,1.613]@{sym2}O-[@{sym2-9}::60]@{sym9}H)%
-[@{sym4-5}::300,1.613]@{sym4}(-[@{sym4-6}::20]@{sym6}H)(%
-[@{sym4-7}::100]@{sym7}H)-[@{sym1-4}::300,1.613]@{sym1}S%
-[@{sym1-8}::60]@{sym8}H}"""
target5 = r"""\chemfig{H-[:340](-[::280]H)-[::80]S-[::240](-[::240])(-[::340]H)-[::80]H}"""


@pytest.fixture(autouse=True)
def mock_pubchem_urlopen(monkeypatch):
    """
    Replace the live PubChem round trip with a canned SDF read from
    tests/data_pubchem/<cid>.sdf, so this file's parametrized cases
    exercise chemfig-rendering logic only, not network access.
    Fixtures were captured once via the real pubchem_url and committed.
    """
    def _fake_urlopen(url, *a, **kw):
        cid = url.rsplit("cid=", 1)[1].split("&")[0]
        sdf_bytes = (FIXTURE_DIR / f"{cid}.sdf").read_bytes()

        class _Resp:
            def read(self_inner):
                return sdf_bytes

        return _Resp()

    monkeypatch.setattr(processor.request, "urlopen", _fake_urlopen)


@pytest.mark.parametrize(
    "input_value,arg1,arg2,expected",
    [
        ("996", "", "", target1),  # phenol
        ("241", "-r", "-u", target2),  # benzene
        (1133, "-u", "-p", target3),  # mercaptoacetic acid
        (1133, "-v", "-g sym", target4),
        (9865, "-y add", "-v", target5),  # thiirane
    ],
)
def test(input_value, arg1, arg2, expected):
    assert mol2chemfig(input_value, arg1, arg2, inline=True) == expected
