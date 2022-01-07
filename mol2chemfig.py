# -*- coding: utf-8 -*-
import sys
from mol2chemfigPy3 import process


success, result = process(raw_args=sys.argv[1:], program_name=sys.argv[0])
if success:
    print(result.render_user())
else:
    print(result)
