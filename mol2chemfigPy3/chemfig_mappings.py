# -*- coding: utf-8 -*-
"""
definitions and code to translate the molecule tree to chemfig

this code will only make sense to you if you are familiar with
the TeX syntax defined by the chemfig package.
"""

import textwrap

BOND_CODE_WIDTH = 50  # space for bonds - generous upfront, will be trimmed at the end
TERSE_LINE_WIDTH = 75  # in terse code format, force linebreaks


def num_round(num, sig):
    """
    round and, if applicable, return integer instead of float
    """
    res = round(num, sig)
    if res == int(res):
        return int(res)
    return res


bond_codes = dict(  # bond_type -> chemfig bond code. defaults to '-'
    double='=',
    triple='~',
    upto='<',
    downto='<:',
    upfrom='>',
    downfrom='>:'
)

bond_type_tikz = dict(  # bond type -> tikz
    link='draw=none',
    either='mcfwavy'
)

bond_styles = dict(  # bond style -> tikz template
    cross='mcfx={%(bgstart)s}{%(bgend)s}',
    double_left='dbl={%(start)s}{%(end)s}',
    double_right='dbr={%(start)s}{%(end)s}',
    triple='trpl={%(start)s}{%(end)s}',
    # combined styles for double, triple and cross
    cross_double_left='dblx={%(start)s}{%(end)s}{%(bgstart)s}{%(bgend)s}',
    cross_double_right='dbrx={%(start)s}{%(end)s}{%(bgstart)s}{%(bgend)s}',
    cross_triple='trplx={%(start)s}{%(end)s}{%(bgstart)s}{%(bgend)s}'
)

bond_style_shortcuts = {  # style short cuts for double bonds in hexagons etc
    "dbr={58}{58}": "drh",
    "dbl={58}{58}": "dlh",
    "dbr={0}{58}": "drhe",
    "dbl={0}{58}": "dlhe",
    "dbr={58}{0}": "drhs",
    "dbl={58}{0}": "dlhs",
    "dbr={0}{0}": "drn",
    "dbl={0}{0}": "dln"
}

macro_templates = dict(  # various custom LaTeX macros

    # templates for charges
    plus_charge=r'\mcfplus',
    minus_charge=r'\mcfminus',

    # template for phantom that forms the end of ring-closing bond
    phantom=r'\phantom{%s}',    # phantom at end of ring-closing bonds

    # template for drawing a circle inside an aromatic ring
    aromatic_circle=r'\mcfcringle{%s}',

    # template for the bond connecting the circle to the atom
    aromatic_circle_bond=r'-[%(angle)s,%(length)s,,,draw=none]',

    # cross bonds
    cross_blank=r'draw=none',
    cross_draw=r'mcfcrossbond',

    # markers identifying atoms and bonds
    marker=r'@{%s}'
)

radical_templates = dict(
    east=r'\lewis{0%s,%s}',
    north=r'\lewis{2%s,%s}',
    west=r'\lewis{4%s,%s}',
    south=r'\lewis{6%s,%s}'
)

atom_templates = dict(
    # templates for atoms, specialized for different numbers and preferred
    # quadrants of attached hydrogen and charges

    # atom numbers
    atom_no=dict(
                empty=(r'\mcfatomno{%(number)s}', 0),
                east=(r'\mcfright{%(element)s}{\mcfatomno{%(number)s}}', 0),
                west=(r'\mcfleft{\mcfatomno{%(number)s}}{%(element)s}', 0),
                north=(r'\mcfabove{%(element)s}{\mcfatomno{%(number)s}}', 0),
                south=(r'\mcfbelow{%(element)s}{\mcfatomno{%(number)s}}', 0)
            ),

    neutral=dict(
                # one hydrogen
                one_h=dict(
                        east=(r'%(element)sH', 1),
                        west=(r'H%(element)s', 2),
                        north=(r'\mcfabove{%(element)s}{H}', 0),
                        south=(r'\mcfbelow{%(element)s}{H}', 0)
                ),

                # multiple hydrogen
                more_h=dict(
                        east=(r'%(element)sH_%(hydrogens)s', 1),
                        west=(r'H_%(hydrogens)s%(element)s', 2),
                        north=(r'\mcfabove{%(element)s}{\mcfright{H}{_%(hydrogens)s}}', 0),
                        south=(r'\mcfbelow{%(element)s}{\mcfright{H}{_%(hydrogens)s}}', 0)
                ),
    ),

    # charged
    charged=dict(
                no_h=dict(
                        top_right=(r'\mcfright{%(element)s}{^{%(charge)s}}', 0),
                        top_left=(r'^{%(charge)s}%(element)s', 2),
                        top_center=(r'\mcfabove{%(element)s}{_{%(charge)s}}', 0),
                        bottom_right=(r'\mcfright{%(element)s}{_{%(charge)s}}', 0),
                        bottom_left=(r'_{%(charge)s}%(element)s', 2),
                        bottom_center=(r'\mcfbelow{%(element)s}{^{%(charge)s}}', 0)
                ),

                # one hydrogen
                one_h=dict(
                        east=(r'%(element)sH^{%(charge)s}', 1),
                        h_west=(r'^{%(charge)s}H%(element)s', 3),
                        north=(r'\mcfaboveright{%(element)s}{H}{^{%(charge)s}}', 0),
                        south=(r'\mcfbelowright{%(element)s}{H}{^{%(charge)s}}', 0)
                ),

                # more hydrogen
                more_h=dict(
                        east=(r'%(element)sH_%(hydrogens)s^{%(charge)s}', 1),
                        west=(r'^{%(charge)s}H_%(hydrogens)s%(element)s', 3),
                        north=(r'\mcfaboveright{%(element)s}{H}{^{%(charge)s}_%(hydrogens)s}', 0),
                        south=(r'\mcfbelowright{%(element)s}{H}{^{%(charge)s}_%(hydrogens)s}', 0)
                )
     )
)


#  helpers for bond formatting

def format_angle(options, angle, parent_angle) -> str:
    """
    format prefix and number for bond angle
    """
    if options['relative_angles'] and parent_angle is not None:
        angle -= parent_angle
        prefix = '::'
    else:
        prefix = ':'

    angle = num_round(angle, options['angle_round'])

    return prefix + str(angle % 360)


def specifier_default(val, default) -> str:
    """
    set bond specifier default values to ""
    """
    if val == default:
        return ""
    return str(val)

# the master bond formatter


def format_bond(options,
                angle,
                parent_angle,
                bond_type,
                clockwise,
                is_last,
                length,
                departure,
                arrival,
                tikz_styles,
                tikz_values,
                marker) -> str:
    """
    render the bond code for one atom; the atom itself is
    rendered separately in format_atom
    """

    # debug(tikz_styles, tikz_values)

    if angle is None:   # angle is None -- first atom only. Is this ever used? Shouldn't
        return ''       # let's try to eliminate once the rest is working

    angle = format_angle(options, angle, parent_angle)

    angle = specifier_default(angle, ':0')

    length = num_round(length, options['bond_round'])
    length = specifier_default(length, 1)

    departure = specifier_default(departure, 0)
    arrival = specifier_default(arrival, 0)

    bond_code = bond_codes.get(bond_type, '-')

    tikz_filled = []

    btt = bond_type_tikz.get(bond_type, None)
    if btt is not None:
        tikz_filled.append(btt)

    if tikz_styles:
        key = '_'.join(sorted(list(tikz_styles)))

        tikz = bond_styles[key] % tikz_values
        tikz_filled.append(tikz)

        if "cross" in key and not is_last:    # departure atom is empty or a phantom, so
            departure = ""                    # at most 1 character. is_last guards against edge case.

    tikz = ','.join(tikz_filled)
    tikz = bond_style_shortcuts.get(tikz, tikz)  # replace tikz with shortcut if available

    specifiers = [angle, length, departure, arrival, tikz]
    specifiers = ','.join(specifiers).rstrip(',')

    if marker:
        specifiers = format_marker(marker) + specifiers

    if specifiers:
        specifiers = '[%s]' % specifiers

    # modify double bonds in non-aromatic rings
    if bond_type == 'double' and clockwise != 0:
        if clockwise == 1:
            modifier = '_'
        else:
            modifier = '^'
    else:
        modifier = ''

    return bond_code + modifier + specifiers


def fill_atom(keys, data, phantom, phantom_pos=0) -> tuple:
    """
    helper for finalizing atom code. phantom_pos is the
    target position of a bond attaching to a phantom;
    currently, this is always 0, but if phantoms
    should become more elaborate, that might change.
    """
    thing = atom_templates[keys[0]]

    # drill down into the template dict
    for key in keys[1:]:
        thing = thing[key]

    template, string_pos = thing
    return template % data, string_pos, phantom, phantom_pos


def format_marker(marker) -> any:
    """
    used for both bonds and atoms
    """
    if marker:
        marker = macro_templates['marker'] % marker
    return marker


def format_atom(options,
                idx,
                element,
                hydrogens,
                charge,
                radical,
                first_quadrant,
                second_quadrant,
                charge_angle) -> tuple:
    """
    render an atom with hydrogens and charges. Return
    - the chemfig code of the rendered atom
    - the string position for incoming bonds to attach to
    - a phantom string to be used for closing rings. We do this
      here because we don't want to duplicate all those case
      distinctions somewhere else. In most cases, the phantom
      string is never used though.
    """

    _mt = macro_templates    # shortcuts
    _at = atom_templates

    # collect elements in a dict that then is used to fill
    # the configured string templates.

    # first, check whether we have a radical
    if radical == 0:
        radical_element = element
    else:
        if radical == 1:
            radical_symbol = '.'
        else:
            radical_symbol = ':'
        if hydrogens:
            radical_quadrant = second_quadrant
        else:
            radical_quadrant = first_quadrant
        radical_element = radical_templates[radical_quadrant] % (radical_symbol, element)

    data = dict(
        number=idx,
        hydrogens=hydrogens,
        element=radical_element,
    )

    # we almost always need the same phantom string, so we prepare it once
    element_phantom = _mt['phantom'] % data['element']

    # deal with atom numbers first
    if options['atom_numbers']:
        if element == 'C' and not options['show_carbons']:
            phantom = _mt['phantom'] % idx
            keys = ('atom_no', 'empty')
            return fill_atom(keys, data, phantom)

        # not an empty carbon
        keys = ('atom_no', first_quadrant)
        return fill_atom(keys, data, element_phantom)

    # full atoms, no numbers

    # neutrals
    if charge == 0:

        # empty carbons. This case is so simple we don't use a template.
        if data['element'] == 'C' and not options['show_carbons'] and (not options['show_methyls'] or hydrogens < 3):
            return '', 0, '', 0

        # next simplest case: neutral atom without hydrogen
        if not hydrogens:
            return data['element'], 0, element_phantom, 0

        # one or more hydrogen
        if hydrogens == 1:
            keys = ('neutral', 'one_h', first_quadrant)
        else:
            keys = ('neutral', 'more_h', first_quadrant)
        return fill_atom(keys, data, element_phantom)

    # at this point, we have a charged atom

    # format dict entry for charge, as it is configurable
    if charge > 0:
        data['charge'] = _mt['plus_charge']
    else:
        data['charge'] = _mt['minus_charge']

    if abs(charge) > 1:
        data['charge'] = str(abs(charge)) + data['charge']

    if not hydrogens:
        keys = ('charged', 'no_h', charge_angle)
    elif hydrogens == 1:
        keys = ('charged', 'one_h', first_quadrant)
    else:
        keys = ('charged', 'more_h', first_quadrant)

    return fill_atom(keys, data, element_phantom)


def format_atom_comment(options,
                        idx) -> str:
    """
    render an optional end-of-line comment after a regular atom
    """
    if options['terse']:
        return ''
    return str(idx)


def format_closure_comment(options,
                           idx) -> str:
    """
    render an optional end of line comment after a ring-closing bond
    """
    if options['terse']:
        return ''
    return '-> %s' % idx


def format_aromatic_ring(options,
                         angle,
                         parent_angle,
                         length,
                         radius) -> (str, str, str):

    values = dict(
                angle=format_angle(options, angle, parent_angle),
                length=specifier_default(length, 1)
             )

    ring_bond_code = macro_templates['aromatic_circle_bond'] % values
    ring_code = macro_templates['aromatic_circle'] % radius

    if options['terse']:
        comment = ''
    else:
        comment = '(o)'

    return ring_bond_code, ring_code, comment


def strip_output(output_list) -> list:
    """
    remove white space and comments
    """
    stripped = []

    for line in output_list:
        stripped.append(line.split('%')[0].strip())

    stripped.reverse()

    chunked = []

    acc = ''

    while stripped:
        popped = stripped.pop()
        if len(acc) + len(popped) > TERSE_LINE_WIDTH:
            chunked.append(acc)
            acc = popped
        else:
            acc += popped
    if acc:
        chunked.append(acc)

    return chunked


def format_output(options, output_list) -> str:
    """
    optionally wrap the translated output into a command,
    to ease inclusion in LaTeX documents with \\input
    """
    # first, do a bit of prettification by removing excessive
    # indentation
    _indent = ' ' * options['indent']

    _out = '\n'.join(output_list)
    _out = textwrap.dedent(_out).splitlines()

    output_list = [_indent + i for i in _out]

    if options['submol_name'] is not None:
        output_list.insert(0, r'\definesubmol{%s}{' % options['submol_name'])
        output_list.append(r'}')

    elif options['chemfig_command']:
        output_list.insert(0, r'\chemfig{')
        output_list.append(r'}')

    if options['terse']:
        output_list = strip_output(output_list)
        joiner = '%\n'
    else:
        joiner = '\n'

    return joiner.join(output_list)
