# -*- coding: utf-8 -*-
import string
from . import chemfig_mappings as cfm
# some atoms should carry their hydrogen to the left, rather than
# to the right. This is applied to solitary atoms, but not to bonded
# functional groups that contain those elements.

hydrogen_lefties = "O S Se Te F Cl Br I At".split()  # I hope these are all ...


class Atom:
    """
    wrapper around toolkit atom object, augmented with coordinates
    helper class for molecule.Molecule
    """
    explicit_characters = set(string.ascii_uppercase + string.digits)

    quadrant_turf = 80  # 80 degrees have to remain free on either side

    quadrants = [  # quadrants for hydrogen placement
        [0, 0, 'east'],
        [1, 180, 'west'],
        [2, 270, 'south'],
        [3, 90, 'north']
    ]

    charge_positions = [  # angles for placement of detached charges
        [0, 15, 'top_right'],
        [1, 165, 'top_left'],
        [2, 90, 'top_center'],
        [3, 270, 'bottom_center'],
        [4, 345, 'bottom_right'],
        [5, 195, 'bottom_left']
    ]

    charge_turf = 50  # reserved angle for charges - needs to be big enough for 2+

    def __init__(self,
                 options,
                 idx,
                 x,
                 y,
                 element,
                 hydrogens,
                 charge,
                 radical,
                 neighbors):
        self.options = options
        self.idx = idx
        self.x = x
        self.y = y
        self.element = element
        self.hydrogens = hydrogens
        self.charge = charge
        self.radical = radical
        self.neighbors = neighbors  # the indexes only
        self.first_quadrant, self.second_quadrant = None, None
        self.string_pos, self.phantom, self.phantom_pos = None, None, None
        self.charge_angle = None
        # angles of all attached bonds - to be populated later
        self.bond_angles = []
        marker = self.options.get('markers', None)
        if marker is not None:
            self.marker = "%s%s" % (marker, self.idx + 1)
        else:
            self.marker = ""

    @staticmethod
    def _score_angle(a, b, turf):
        """
        helper. calculates absolute angle between a and b.
        0 <= angle <= 180
        then compares to turf angle and returns a score > 0
        if angle falls within turf.
        """
        diff = (a - b) % 360
        angle = min(diff, 360 - diff)
        return (max(0, turf - angle)) ** 2

    def _score_angles(self, choices, turf):
        """
        backend for score_angles
        """
        aux = []
        for priority, choice_angle, name in choices:
            score = 0
            for bond_angle in self.bond_angles:
                score += self._score_angle(choice_angle, bond_angle, turf)
            aux.append((score, priority, name))
        aux.sort()
        named = [a[-1] for a in aux]
        return named

    def score_angles(self):
        """
        determine which positions

        We use one score for the placement of hydrogen w/ or w/o charge,
        and a separate one for the placement of charges only.

        Atoms: precedence east, west, south, north
               tolerated impingement 10 degrees

        Charges: precedence top right, top left, top straight,
                 bottom straight, others
        """
        if len(self.bond_angles) > 0:  # this atom is bonded
            quadrants = self._score_angles(self.quadrants, self.quadrant_turf)
            self.first_quadrant = quadrants[0]
            self.second_quadrant = quadrants[1]  # 2nd choice may be used for radical electrons

        else:  # this atom is solitary
            if self.element in hydrogen_lefties:
                self.first_quadrant = 'west'
                self.second_quadrant = 'east'
            else:
                self.first_quadrant = 'east'
                self.second_quadrant = 'west'

        self.charge_angle = self._score_angles(self.charge_positions, self.charge_turf)[0]

    def render_phantom(self):
        """
        render a bond that closes a ring or loop, or for
        late-rendered cross bonds. The target atom
        is represented by a phantom.

        This relies on .render() having been called earlier, which
        it will be - atoms always precede their phantoms during
        molecule tree traversal.
        """
        atom_code = self.phantom
        comment_code = cfm.format_closure_comment(
            self.options,
            self.idx + 1,
        )
        return atom_code, comment_code

    def render(self):
        """
        render the atom and a comment
        """
        atom_code, self.string_pos, self.phantom, self.phantom_pos = cfm.format_atom(
            self.options,
            self.idx + 1,
            self.element,
            self.hydrogens,
            self.charge,
            self.radical,
            self.first_quadrant,
            self.second_quadrant,
            self.charge_angle,
        )

        comment_code = cfm.format_atom_comment(
            self.options,
            self.idx + 1,
        )
        marker_code = cfm.format_marker(self.marker)
        if marker_code:
            comment_code = " "  # force an empty comment, needed after markers
        return marker_code + atom_code, comment_code
