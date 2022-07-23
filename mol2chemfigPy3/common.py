# -*- coding: utf-8 -*-
"""
common settings and a bit of infrastructure
"""
from .options import getParser

program_version = "1.5.7"

# pubchem url for retrieving sdf for numerical IDs
pubchem_url = (
    r"http://pubchem.ncbi.nlm.nih.gov/summary/summary.cgi?cid=%s&disopt=DisplaySDF"
)

_version_blurb = """
%(program_name)s version %(version)s

mol2chemfig generates chemfig code from molfiles.
For more information, type '%(program_name)s --help'.
"""

_lua_version_blurb = """
This is version %(client_version)s of %(program_name)s,
the Lua web client for the mol2chemfig server. The
server is running version %(server_version)s of mol2chemfig;
server and client version may differ.

%(program_name)s generates chemfig code from molfiles.
For more information, type '%(program_name)s --help'.
"""

_help_blurb = """
%(program_name)s version %(version)s, originally by Eric Brefo-Mensah and Michael Palmer;
Re-written in python3 by Nianze A. TAO (Omozawa SUENO) in 2021.*
*Visit https://augus1999.github.io/mol2chemfigPy3/ for more details.
%(program_name)s generates chemfig code from molfiles. Usage example:

%(program_name)s --angle=45 --aromatic-circles somefile.mol

Options:
"""


def version_text(program_name="mol2chemfigPy3", version=program_version) -> str:
    return _version_blurb % locals()


def help_text(program_name="mol2chemfigPy3", version=program_version) -> str:
    msg = _help_blurb % locals()
    msg += getParser().format_help(indent=32, linewidth=75, separator="")
    return msg


def lua_version_text(program_name, client_version) -> str:
    server_version = program_version
    return _lua_version_blurb % locals()


# the settings dict contains a number of fixed settings that can not
# be overridden from the command line. A copy of this dict will
# augmented with command line options and passed around during processing.

settings = dict(
    # input mode: auto, molfile, molblock, smilesfile, smiles
    input_mode="auto",
    # use relative angles
    relative_angles=False,
    # round bond lengths to this many decimal digits
    bond_round=3,
    # round angles to this many digits
    angle_round=1,
    # tolerance for angle impingement on atom quadrants, range 0 to 1
    quadrant_tolerance=0.1,
)


class MCFError(Exception):
    """
    this flags an anticipated error due to faulty user input.
    """

    def __init__(self, text: any):
        self.text = str(text)

    def __str__(self):
        return self.text


class Counter:
    """
    a simple Counter class, just to remove the dependency on version 2.7
    (which provides one in module collections)
    """

    def __init__(self, lst: list):
        self._d = {}

        for val in lst:
            if not (val in self._d):
                self._d[val] = 0

            self._d[val] += 1

    def most_common(self) -> any:
        """
        return the most common object

        :return: an object (any type)
        """
        lst = list(self._d.items())
        lst.sort(key=lambda pair: pair[1])

        return lst[-1][0]
