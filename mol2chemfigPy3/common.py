"""
common settings and a bit of infrastructure
"""
# import sys
from .options import getParser

_debug = False

# _debug_file = sys.stderr
if _debug:
    _debug_file = open('/data/code/mol2chemfig/bugs/dbg', 'w')

program_version = '1.4'


def debug(*args):
    if not _debug:
        return
    args = [str(a) for a in args]
    print(" ".join(args), file=_debug_file)


class MCFError(Exception):
    """
    this flags an anticipated error due to faulty user input.
    """
    pass


# pubchem url for retrieving sdf for numerical IDs
pubchem_url = r"http://pubchem.ncbi.nlm.nih.gov/summary/summary.cgi?cid=%s&disopt=DisplaySDF"

_version_blurb = '''
%(progname)s version %(version)s

mol2chemfig generates chemfig code from molfiles.
For more information, type '%(progname)s --help'.
'''

_lua_version_blurb = '''
This is version %(client_version)s of %(progname)s,
the Lua web client for the mol2chemfig server. The
server is running version %(server_version)s of mol2chemfig;
server and client version may differ.

%(progname)s generates chemfig code from molfiles.
For more information, type '%(progname)s --help'.
'''


def version_text(progname='mol2chemfig', version=program_version):
    return _version_blurb % locals()


_help_blurb = '''\
%(progname)s v. %(version)s,  by Eric Brefo-Mensah and Michael Palmer
%(progname)s generates chemfig code from molfiles. Usage example:

%(progname)s --angle=45 --aromatic-circles somefile.mol

Options:
'''


def help_text(progname="mol2chemfig", version=program_version):
    msg = _help_blurb % locals()
    msg += getParser().format_help(indent=32, linewidth=75, separator='')

    return msg


def lua_version_text(progname, client_version):
    server_version = program_version
    return _lua_version_blurb % locals()


# the settings dict contains a number of fixed settings that can not
# be overridden from the command line. A copy of this dict will
# augmented with command line options and passed around during processing.

settings = dict(
    # input mode: auto, molfile, molblock, smilesfile, smiles
    input_mode='auto',

    # use relative angles
    relative_angles=False,

    # round bond lengths to this many decimal digits
    bond_round=3,

    # round angles to this many digits
    angle_round=1,

    # tolerance for angle impingement on atom quadrants, range 0 to 1
    quadrant_tolerance=0.1,
)


class Counter(object):
    """
    a simple Counter class, just to remove the dependency on version 2.7
    (which provides one in module collections)
    """

    def __init__(self, lst):
        self._d = {}

        for val in lst:
            if not (val in self._d):
                self._d[val] = 0

            self._d[val] += 1

    def most_common(self):
        lst = list(self._d.items())
        lst.sort(key=lambda pair: pair[1])

        return lst[-1][0]
