import platform
from glob import glob
from pathlib import Path
import pyan

cwd = Path(__file__).parent
fns = glob(str((cwd.parent / "mol2chemfigPy3/*.py").resolve()))
html = pyan.create_callgraph(
    filenames=fns,
    namespace="mol2chemfigPy3",
    format="svg",
    annotated=True,
    grouped=True,
    root=(cwd.parent / "mol2chemfigPy3").resolve().__str__(),
)
print(cwd_n := cwd.parent.resolve().__str__())
if platform.system() == "Windows":
    cwd_n = cwd_n.replace("/", "").replace("\\", "")
    html = html.replace(cwd_n + (a := "mol2chemfigPy3"), a + "/")
else:
    html = html.replace(cwd_n + "/", "")
with open(cwd / "section/4_callgraph.svg", "w") as f:
    f.write(html)
