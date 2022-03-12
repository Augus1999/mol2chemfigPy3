# -*- coding: utf-8 -*-
# option declarations. The options will be used to update the
# settings dict in module common.
from .optionparser import (
    OptionParser,
    BoolOption,
    IntOption,
    FloatOption,
    StringOption,
    SelectOption,
    RangeOption,
)


def getParser() -> OptionParser:
    """
    make sure the parser is created anew on each request

    :return: OptionParser object
    """
    parser = OptionParser()
    parser.append(
        BoolOption(
            "help",
            "h",
            default=False,
            help_text="Print help message and exit.",
        )
    )

    parser.append(
        BoolOption(
            "version",
            "b",
            default=False,
            help_text="Print program version and exit.",
        )
    )

    parser.append(
        SelectOption(
            "input",
            "i",
            key="input",
            default="file",
            valid_range="direct file pubchem".split(),
            help_text="""
        How to interpret the argument. 
        With 'file', mol2chemfig expects a filename.
        With 'direct', the argument is interpreted directly; don't forget to put quotes around it.
        With 'pubchem', the argument is treated as an identifier for the PubChem database.
        """,
        )
    )

    parser.append(
        BoolOption(
            "terse",
            "z",
            default=False,
            help_text="""
        Remove all whitespace and comments from the output.
        If you can still read it afterwards, Bill Gates wants your resume.
        """,
        )
    )

    parser.append(
        BoolOption(
            "strict",
            "r",
            default=True,
            help_text="""
        Abide by Indigo's chemical structure validation.
        If true, mol2chemfig will fail if Indigo reports that something is wrong with the molecule.
        If false, mol2chemfig will ignore such errors.
        """,
        )
    )

    parser.append(
        IntOption(
            "indent",
            "d",
            default=4,
            help_text="""
        Number of spaces to use for indenting molecule branches in generated code.
        Without effect when 'terse' option is passed.
        Affects only the generated tex code, not the rendered molecule.
        """,
        )
    )

    parser.append(
        BoolOption(
            "recalculate-coordinates",
            "u",
            key="recalculate_coordinates",
            help_text="""
        Discard existing coordinate and calculate new ones from covalent structure.
        For smiles input, this is performed implicitly.
        """,
        )
    )

    parser.append(
        FloatOption(
            "angle",
            "a",
            key="rotate",
            default=0.0,
            help_text="Rotate molecule counterclockwise by this angle.",
        )
    )

    parser.append(
        BoolOption(
            "relative-angles",
            "v",
            key="relative_angles",
            default=False,
            help_text="Use relative bond angles.",
        )
    )

    parser.append(
        BoolOption(
            "flip",
            "p",
            key="flip_horizontal",
            default=False,
            help_text="Flip the structure horizontally.",
        )
    )

    parser.append(
        BoolOption(
            "flop",
            "q",
            key="flip_vertical",
            default=False,
            help_text="Flip the structure vertically.",
        )
    )

    parser.append(
        BoolOption(
            "show-carbons",
            "c",
            key="show_carbons",
            help_text="Show element symbol for carbon atoms.",
        )
    )

    parser.append(
        BoolOption(
            "show-methyls",
            "m",
            key="show_methyls",
            help_text="Show element symbols for methyl groups (implied if show-carbons is True).",
        )
    )

    parser.append(
        SelectOption(
            "hydrogens",
            "y",
            key="hydrogens",
            valid_range="keep add delete".split(),
            help_text="""
        How to deal with explicit hydrogen atoms.
        One of 'keep', 'add' or 'delete'. 
        Note that 'add' will also trigger calculation of new coordinates for the entire molecule.
        Option 'keep' does nothing.
        """,
        )
    )

    parser.append(
        BoolOption(
            "aromatic-circles",
            "o",
            key="aromatic_circles",
            default=False,
            help_text="Draw circles instead of double bonds inside aromatic rings.",
        )
    )

    parser.append(
        BoolOption(
            "fancy-bonds",
            "f",
            key="fancy_bonds",
            default=False,
            help_text="Draw fancier double and triple bonds.",
        )
    )

    parser.append(
        StringOption(
            "markers",
            "g",
            help_text="""
        Give each atom and each bond a unique marker that can be used for attaching electron movement arrows.
        With value 'a', atom 2 will be labeled @{a2}, and its bond to atom 5 @{a2-5}.
        """,
        )
    )

    parser.append(
        BoolOption(
            "atom-numbers",
            "n",
            key="atom_numbers",
            default=False,
            help_text="""
        Show the molfile number of each atom next to it.
        When this option is set, charges and implicit hydrogen will not be shown.
        """,
        )
    )

    parser.append(
        SelectOption(
            "bond-scale",
            "s",
            key="bond_scale",
            valid_range="normalize keep scale".split(),
            help_text="""
        How to scale the lengths of bonds.
        (one of 'keep', 'scale', or 'normalize')
        """,
        )
    )

    parser.append(
        FloatOption(
            "bond-stretch",
            "t",
            key="bond_stretch",
            default=1.0,
            help_text="""
        Used as scaling factor (with --bond-scale=scale)
        or average (with --bond-scale=normalize) for bond lengths.
        """,
        )
    )

    parser.append(
        BoolOption(
            "wrap-chemfig",
            "w",
            key="chemfig_command",
            help_text="Wrap generated code into \\chemfig{...} command.",
        )
    )

    parser.append(
        StringOption(
            "submol-name",
            "l",
            key="submol_name",
            help_text="If a name is given, wrap generated code into chemfig \\definesubmol{name}{...} command.",
        )
    )

    parser.append(
        IntOption(
            "entry-atom",
            "e",
            key="entry_atom",
            default=None,
            help_text="""
        Number of first atom to be rendered.
        Relevant only if generated code is to be used as sub-molecule.
        """,
        )
    )

    parser.append(
        IntOption(
            "exit-atom",
            "x",
            key="exit_atom",
            default=None,
            help_text="""
        Number of last atom to be rendered.
        Relevant only if generated code is to be used as sub-molecule.
        """,
        )
    )

    parser.append(
        RangeOption(
            "cross-bond",
            "k",
            key="cross_bond",
            default=None,
            help_text="""
        Specify bonds that should be drawn on top of others they cross over.
        Give the start and the end atoms.
        Example for one bond: --cross-bond=5-6
        Example for two bonds: --crossbond=4-8,12-13
        """,
        )
    )

    return parser
