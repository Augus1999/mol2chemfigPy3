import sys
from mol2chemfigPy3.processor import process


success, result = process(rawargs=sys.argv[1:], progname=sys.argv[0])
if success:
    print(result.render_user())
else:
    print(result, file=sys.stderr)
