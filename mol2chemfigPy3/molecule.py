# -*- coding: utf-8 -*-
# parse a molfile molecule and render to chemfig code
import math
from typing import Optional, Union, Tuple, List, Dict
from indigo import IndigoException, IndigoObject
from . import chemfig_mappings as cfm
from .common import MCFError, Counter
from .atom import Atom
from .bond import Bond, DummyFirstBond, AromaticRingBond, compare_positions


class Molecule:
    bond_scale = 1.0  # can be overridden by user option
    exit_bond = None  # the first bond in the tree that connects to the exit atom

    def __init__(self, options: Dict, tkmol: IndigoObject):
        self.options = options
        self.tkmol = tkmol

        self.atoms = self.parseAtoms()

        # now it's time to flip and flop the coordinates
        for atom in list(self.atoms.values()):
            if self.options["flip_horizontal"]:
                atom.x = -atom.x
            if self.options["flip_vertical"]:
                atom.y = -atom.y

        self.bonds, self.atom_pairs = self.parseBonds()

        # work out the angles for each atom - this is used for
        # positioning of implicit hydrogen and charges.

        for connection, bond in list(self.bonds.items()):
            first_idx, last_idx = connection
            self.atoms[first_idx].bond_angles.append(bond.angle)

        # this would be the place to work out the placement of the second
        # and third strokes.

        # connect fragments, if any, with invisible bonds. By doing this
        # AFTER assigning bond angles, we prevent these invisible bonds
        # from interfering with placement of hydrogen or charges.
        self.connect_fragments()  # connect fragments or isolated atoms

        # arrange the bonds into a tree
        self.seen_atoms = set()
        self.seen_bonds = set()

        self.entry_atom, self.exit_atom = self.pickFirstLastAtoms()
        self.root = self.parseTree(start_atom=None, end_atom=self.entry_atom)

        if len(self.atoms) > 1:
            if self.exit_atom is None:  # pick a default exit atom if needed
                self.exit_bond = self.default_exit_bond()
                self.exit_atom = self.exit_bond.end_atom

            # flag all atoms between the entry atom and the exit atom - these
            # will be part of the trunk, all others will be rendered as branches
            if self.entry_atom is not self.exit_atom:
                flagged_bond = self.exit_bond

                while flagged_bond.end_atom is not self.entry_atom:
                    flagged_bond.is_trunk = True
                    flagged_bond = flagged_bond.parent

            # process cross bonds
            if self.options["cross_bond"] is not None:
                self.process_cross_bonds()

            # adjust bond lengths
            self.scaleBonds()

            # modify bonds in rings
            self.annotateRings()

        # let each atom work out its preferred quadrant for placing
        # hydrogen or charges
        for atom in list(self.atoms.values()):
            atom.score_angles()

        # finally, render the thing and cache the result.
        self._rendered = self.render()

    def link_atoms(self, x: int, y: int) -> None:
        """
        connect atoms with indexes x and y using a pseudo bond.
        Helper for connect_fragments

        :param x: x index
        :param y: y index
        :return: None
        """
        start_atom = self.atoms[x]
        end_atom = self.atoms[y]

        bond = Bond(self.options, start_atom, end_atom)
        bond.set_link()

        self.bonds[(x, y)] = bond
        self.bonds[(y, x)] = bond.invert()

        start_atom.neighbors.append(y)
        end_atom.neighbors.append(x)

    def connect_fragments(self) -> None:
        """
        connect multiple fragments, using link bonds across their
        last and first atoms, respectively.

        :return: None
        """
        fragments = self.molecule_fragments()

        if len(fragments) > 1:

            for head, tail in zip(fragments[:-1], fragments[1:]):
                head_last = head[-1][-1]
                tail_first = tail[0][0]

                self.link_atoms(head_last, tail_first)

        # now look for orphaned single atoms
        atoms = set(self.atoms.keys())

        bonded = set()
        for pair in self.atom_pairs:
            bonded.update(pair)

        un_bonded = list(atoms - bonded)

        if un_bonded:
            if fragments:
                anchor = fragments[-1][-1][-1]
            else:  # several atoms, but no bonds
                anchor, un_bonded = un_bonded[0], un_bonded[1:]

            for atom in un_bonded:
                self.link_atoms(anchor, atom)

    def molecule_fragments(self) -> List:
        """
        identify unconnected fragments in the molecule.
        used by connect_fragments

        :return: fragments
        """

        def split_pairs(pair_list: List) -> Tuple[List, List]:
            """
            break up pair_list into one list that contains all pairs
            that are connected, directly or indirectly, to the first
            pair in the list, and another list containing the rest.
            """
            first, _rest = pair_list[0], pair_list[1:]
            connected_atoms = set(first)

            connected_pairs = [first]

            while True:
                unconnected = []

                for r in _rest:
                    s = set(r)

                    if connected_atoms & s:
                        connected_atoms |= s
                        connected_pairs.append(r)
                    else:
                        unconnected.append(r)

                if len(unconnected) == len(
                    _rest
                ):  # no new pairs found in this loop iteration
                    return connected_pairs, unconnected
                else:
                    _rest = unconnected

        fragments = []

        atom_pairs = self.atom_pairs[:]

        if len(atom_pairs) == 0:
            return []
        elif len(atom_pairs) == 1:
            return [atom_pairs]

        while True:
            connected, rest = split_pairs(atom_pairs)
            fragments.append(connected)

            if not rest:
                return fragments
            else:
                atom_pairs = rest

    def treebonds(self, root: bool = False) -> List:
        """
        return a list with all bonds in the molecule tree

        :param root: whether include the first bond
        :return: [bond_1, bond_2, ...]
        """
        all_bonds = []

        def recurse(rt):
            all_bonds.append(rt)
            for d in rt.descendants:
                recurse(d)

        recurse(self.root)

        if not root:
            all_bonds = all_bonds[1:]

        return all_bonds

    def process_cross_bonds(self) -> None:
        """
        if cross bonds have been declared:
        1. tag the corresponding bonds within the tree as no-ops
        2. create a ghost-bond connection from exit_atom to start atom
        3. create a drawn duplicate of the cross bond
        4. append 2 and 3 as branch to the exit atom

        this is unfortunately all a little hackish.

        :return: None
        """
        cross_bonds = self.options["cross_bond"]

        for start1, end1 in cross_bonds:
            start = start1 - 1
            end = end1 - 1

            # retrieve the matching bond that's in the parse tree
            for combo in ((start, end), (end, start)):
                if combo in self.seen_bonds:
                    bond = self.bonds[combo]
                    break
            else:  # referenced bond doesn't exist
                raise MCFError(f"bond {start1}-{end1} doesn't exist")

            # very special case: the bond _might_ already be the very
            # last one to be rendered - then we just tag it
            if self.exit_bond.descendants and bond is self.exit_bond.descendants[-1]:
                bond.set_cross(last=True)
                continue

            # create a copy of the bond that will be rendered later
            bond_copy = bond.clone()

            # tag original bond as no-op
            bond.set_link()

            # modify bond copy
            bond_copy.set_cross()
            bond_copy.to_phantom = True  # don't render atom again
            bond_copy.descendants = []  # forget copied descendants

            if bond_copy.start_atom is not self.exit_atom:  # usual case
                # create a pseudo bond from the exit atom to the start atom
                # pseudo bond will not be drawn, serves only to "move the pen"
                pseudo_bond = Bond(
                    self.options,
                    self.exit_atom,
                    bond_copy.start_atom,
                )

                pseudo_bond.set_link()
                pseudo_bond.to_phantom = True  # don't render the atom, either

                bond_copy.parent = pseudo_bond
                pseudo_bond.descendants.append(bond_copy)

                pseudo_bond.parent = self.exit_bond
                self.exit_bond.descendants.append(pseudo_bond)

            else:  # occasionally, the molecule's exit atom may be the starting point of the elevated bond
                self.exit_bond.descendants.append(bond_copy)

    def default_exit_bond(self) -> Bond:
        """
        pick the bond and atom that is at the greatest distance from
        the entry atom along the parsed molecule tree. This
        must be one of the leaf atoms, obviously.

        :return: the most distant bond
        """
        scored = []
        bonds = {}
        for bond in self.treebonds():
            if bond.to_phantom:  # don't pick phantom atoms as exit
                continue

            distance = 0

            the_bond = bond

            while the_bond is not None and the_bond.end_atom is not self.entry_atom:
                distance += 1
                the_bond = the_bond.parent

            scored.append((distance, len(bond.descendants)))
            bonds[(distance, len(bond.descendants))] = bond
        scored.sort()
        bond_out = bonds[scored[-1]]
        return bond_out

    def pickFirstLastAtoms(self) -> Tuple[Optional[Atom], Optional[Atom]]:
        """
        If the first atom is not given, we try to pick one
        that has only one bond to the rest of the molecule,
        so that only the first angle is absolute.

        :return: (entry atom, exit atom)
        """
        if self.options["entry_atom"] is not None:
            entry_atom = self.atoms.get(self.options["entry_atom"] - 1)  # -> zero index
            if entry_atom is None:
                raise MCFError("Invalid entry atom number")

        else:  # pick a default atom with few neighbors
            atoms = list(self.atoms.values())
            atoms.sort(key=lambda atom: len(atom.neighbors))
            entry_atom = atoms[0]

        if self.options["exit_atom"] is not None:
            exit_atom = self.atoms.get(self.options["exit_atom"] - 1)  # -> zero index
            if exit_atom is None:
                raise MCFError("Invalid exit atom number")
        else:
            exit_atom = None

        return entry_atom, exit_atom

    def parseAtoms(self) -> Dict:
        """
        Read some attributes from the toolkit atom object

        :return: a dict containing wrapped atoms
        """
        # wrap all atoms and supply coordinates
        wrapped_atoms = {}

        for ra in self.tkmol.iterateAtoms():
            idx = ra.index()
            element = ra.symbol()

            try:
                hydrogens = ra.countImplicitHydrogens()
            except IndigoException:
                if self.options["strict"]:
                    raise
                hydrogens = 0

            charge = ra.charge()
            radical = ra.radicalElectrons()

            neighbors = [na.index() for na in ra.iterateNeighbors()]

            x, y, z = ra.xyz()

            wrapped_atoms[idx] = Atom(
                self.options,
                idx,
                x,
                y,
                element,
                hydrogens,
                charge,
                radical,
                neighbors,
            )

        return wrapped_atoms

    def parseBonds(self) -> Tuple[Dict, List]:
        """
        read some bond attributes

        :return: (bonds, atom pairs)
        """
        bonds = {}  # dictionary with bond objects, both orientations
        atom_pairs = []  # atom index pairs only, unique

        for bond in self.tkmol.iterateBonds():
            # start, end, bond_type, stereo = numbers
            start = bond.source().index()
            end = bond.destination().index()

            bond_type = bond.bondOrder()  # 1,2,3,4 for single, double, triple, aromatic
            stereo = bond.bondStereo()

            start_atom = self.atoms[start]
            end_atom = self.atoms[end]

            bond = Bond(self.options, start_atom, end_atom, bond_type, stereo)

            # we store both orientations of the bond, since we don't know yet
            # which way it will be used
            bonds[(start, end)] = bond
            bonds[(end, start)] = bond.invert()

            atom_pairs.append((start, end))

        return bonds, atom_pairs

    def parseTree(self, start_atom: Optional[Atom], end_atom: Atom) -> Optional[Bond]:
        """
        recurse over atoms in molecule to create a tree of bonds

        :param start_atom: the start atom (can be None)
        :param end_atom: the end atom
        :return: Bond object
        """
        end_idx = end_atom.idx
        start_idx = None
        if start_atom is None:  # this is the first atom in the molecule
            bond = DummyFirstBond(self.options, end_atom=end_atom)

        else:
            start_idx = start_atom.idx

            # guard against reentrant bonds. Can those even still happen?
            # apparently they can, even if I don't really understand how.
            if (start_idx, end_idx) in self.seen_bonds or (
                end_idx,
                start_idx,
            ) in self.seen_bonds:
                return None

            # if we get here, the bond is not in the tree yet
            bond = self.bonds[(start_idx, end_idx)]

            # flag it as known
            self.seen_bonds.add((start_idx, end_idx))

            # detect bonds that close rings, and tell them render
            # with phantom atoms
            if end_idx in self.seen_atoms:
                bond.to_phantom = True
                return bond

        # flag end atom as known
        self.seen_atoms.add(end_idx)

        if end_atom is self.exit_atom:
            self.exit_bond = bond

        # recurse over the neighbors of the end atom
        for ni in end_atom.neighbors:
            if start_atom and ni == start_idx:  # don't recurse backwards
                continue

            next_atom = self.atoms[ni]
            next_bond = self.parseTree(end_atom, next_atom)

            if next_bond is not None:
                next_bond.parent = bond
                bond.descendants.append(next_bond)

        return bond

    def _getBond(self, tk_bond) -> Bond:
        """
        helper for aromatizeRing: find bond in parse tree that
        corresponds to toolkit bond

        :param tk_bond: toolkit bond
        :return: Bond object
        """
        start_idx = tk_bond.source().index()
        end_idx = tk_bond.destination().index()

        if (start_idx, end_idx) in self.seen_bonds:
            return self.bonds[(start_idx, end_idx)]

        # the bond must be going the other way ...
        return self.bonds[(end_idx, start_idx)]

    def aromatizeRing(
        self, ring, center_x: Union[float, int], center_y: Union[float, int]
    ) -> None:
        """
        render a ring that is aromatic and is a regular polygon

        :return: None
        """
        # first, set all bonds to aromatic
        ring_bonds = list(ring.iterateBonds())
        bond = None
        for tk_bond in ring_bonds:
            bond = self._getBond(tk_bond)
            bond.bond_type = "aromatic"

        # any bond can serve as the anchor for the circle,
        # so we'll just use the last one from the loop
        atom = bond.end_atom

        outer_r, angle = compare_positions(atom.x, atom.y, center_x, center_y)
        # angle is based on raw coordinates - adjust for user-set rotation
        angle += self.options["rotate"]

        # outer_r calculated from raw coordinates, must be adjusted
        # for bond scaling that may have taken place
        outer_r *= self.bond_scale

        alpha = math.pi / 2 - math.pi / len(ring_bonds)
        inner_r = math.sin(alpha) * outer_r

        arb = AromaticRingBond(self.options, bond, angle, outer_r, inner_r)
        bond.descendants.append(arb)

    def annotateRing(self, ring, is_aromatic: bool) -> None:
        """
        determine center, symmetry and aromatic character of ring
        I wonder if indigo would tell us directly about these ...

        annotate double bonds in rings, or alternatively decorate
        ring with aromatic circle.

        :param ring: ring
        :param is_aromatic: whether is aromatic molecule
        :return: None
        """
        atoms = set()
        bond_lengths = []
        bonds = []

        for tk_bond in ring.iterateBonds():
            bond = self._getBond(tk_bond)
            bonds.append(bond)

            atoms.add(self.atoms[bond.start_atom.idx])
            atoms.add(self.atoms[bond.end_atom.idx])
            bond_lengths.append(bond.length)

        if len(bonds) > 8:  # large rings may foul things up, so we skip them.
            return

        bl_max = max(bond_lengths)
        bl_spread = (bl_max - min(bond_lengths)) / bl_max

        # determine ring center
        center_x = sum([atom.x for atom in atoms]) / len(atoms)
        center_y = sum([atom.y for atom in atoms]) / len(atoms)

        # compare distances from center. Also remember atoms and bond
        # angles; if the ring ends up being aromatized, we flag those
        # angles as occupied (by the fancy circle inside the ring).
        atom_angles = []
        center_distances = []

        for atom in atoms:
            length, angle = compare_positions(atom.x, atom.y, center_x, center_y)
            center_distances.append(length)
            atom_angles.append((atom, angle))

        cd_max = max(center_distances)
        cd_spread = (cd_max - min(center_distances)) / cd_max

        tolerance = 0.05
        is_symmetric = cd_spread <= tolerance and bl_spread <= tolerance

        if is_aromatic and is_symmetric and self.options["aromatic_circles"]:
            # ring meets all requirements to be displayed with circle inside
            self.aromatizeRing(ring, center_x, center_y)
            # flag bond angles as occupied
            for atom, angle in atom_angles:
                atom.bond_angles.append(angle)

        else:  # flag orientation individual bonds - will influence rendering of double bonds
            for bond in bonds:
                bond.is_clockwise(center_x, center_y)

    def annotateRings(self) -> None:
        """
        modify double bonds in rings. In aromatic rings, we optionally
        do away with double bonds altogether and draw a circle instead

        :return: None
        """
        self.tkmol.aromatize()

        all_rings = []
        rings = {}
        _all_rings = []
        for key, ring in enumerate(self.tkmol.iterateSSSR()):
            # bond-order == 4 means "aromatic"; all rings bonds must be aromatic
            is_aromatic = all(bond.bondOrder() == 4 for bond in ring.iterateBonds())
            all_rings.append((is_aromatic, key))
            rings[(is_aromatic, key)] = ring

        # prefer aromatic rings to non-aromatic ones, so that double bonds on
        # fused rings go preferably into aromatic rings
        all_rings.sort()
        for i in all_rings:
            _all_rings.append((i[0], rings[i]))

        for is_aromatic, ring in reversed(_all_rings):
            self.annotateRing(ring, is_aromatic)

    def scaleBonds(self) -> None:
        """
        scale bonds according to user options

        :return: None
        """
        if self.options["bond_scale"] == "keep":
            pass

        elif self.options["bond_scale"] == "normalize":
            lengths = [bond.length for bond in self.treebonds()]
            lengths = [round(i, self.options["bond_round"]) for i in lengths]
            lengths = Counter(lengths)
            self.bond_scale = self.options["bond_stretch"] / lengths.most_common()

        elif self.options["bond_scale"] == "scale":
            self.bond_scale = self.options["bond_stretch"]

        for bond in self.treebonds():
            bond.length = self.bond_scale * bond.length

    def render(self) -> List:
        """
        render molecule to chemfig

        :return: a list containing rendered bonds
        """
        output = []
        self._render(output, bond=self.root, level=0)

        return output

    def render_user(self) -> str:
        """
        returns code formatted according to user options

        :return: formatted code
        """
        return cfm.format_output(self.options, self._rendered)

    def render_server(self) -> str:
        """
        returns code formatted for server-side PDF generation

        :return: formatted code
        """
        # override some options
        params = dict(self.options)
        params["submol_name"] = None
        # params['terse'] = False  # why?
        params["chemfig_command"] = True

        return cfm.format_output(params, self._rendered)

    def _renderBranches(self, output: List, level: int, bonds: List) -> None:
        """
        render a list of branching bonds indented and inside enclosing brackets.

        :param output: [...]
        :param level: level
        :param bonds: [Bond_1, Bond_2,...]
        :return: None
        """
        branch_indent = self.options["indent"]

        for bond in bonds:
            output.append("(".rjust(level * branch_indent + cfm.BOND_CODE_WIDTH))
            self._render(output, bond, level)
            output.append(")".rjust(level * branch_indent + cfm.BOND_CODE_WIDTH))

    def _render(
        self,
        output: List,
        bond: Union[Bond, DummyFirstBond, AromaticRingBond],
        level: int,
    ) -> None:
        """
        recursively render the molecule.

        :param output: an empty list
        :param bond: Bond object
        :param level: level
        :return: None
        """
        output.append(bond.render(level))
        branches = bond.descendants

        if bond is self.exit_bond:  # wrap all downstream bonds in branch
            self._renderBranches(output, level + 1, branches)

        elif branches:  # prioritize bonds on the trunk from entry to exit
            for i, branch in enumerate(branches):
                if branch.is_trunk:
                    first = branches.pop(i)
                    break
            else:
                first = branches.pop(0)

            self._renderBranches(output, level + 1, branches)
            self._render(output, first, level)

    def dimensions(self) -> Tuple[float, float]:
        r"""
        this calculates the approximate width and height
        of the rendered molecule, in units of chemfig
        standard bond length (multiply with chemfig
        \setatomsep parameter to obtain the physical size).

        It is only used for server side PDF generation,
        but maybe someone will have another use for it.

        :return: (width, height)
        """
        min_x = max_x = min_y = max_y = None

        alpha = self.options["rotate"]
        alpha *= math.pi / 180

        sin_alpha = math.sin(alpha)
        cos_alpha = math.cos(alpha)

        for atom in list(self.atoms.values()):
            x, y = atom.x, atom.y

            xt = x * cos_alpha - y * sin_alpha
            yt = x * sin_alpha + y * cos_alpha

            if min_x is None or xt < min_x:
                min_x = xt
            if max_x is None or xt > max_x:
                max_x = xt
            if min_y is None or yt < min_y:
                min_y = yt
            if max_y is None or yt > max_y:
                max_y = yt

        x_size = (max_x - min_x) * self.bond_scale
        y_size = (max_y - min_y) * self.bond_scale

        return x_size, y_size
