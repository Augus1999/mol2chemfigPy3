# -*- coding: utf-8 -*-
"""
accept input from command line or through the web and
return the result.
"""
import os.path
import traceback
from urllib import request
from typing import Union, List, Tuple
from indigo import Indigo, IndigoException, IndigoObject
from . import common, options, molecule


class HelpError(common.MCFError):
    def __init__(self, text: any):
        self.text = str(text)  # convert error messages to string

    def __str__(self):
        return self.text


class Processor:
    """
    parses input and invokes backend, returns result
    """

    def __init__(
        self,
        raw_args: Union[List, str, None],
        data: str,
        form_fields: any,
        program_name: str,
        web_form: bool,
        rpc: bool,
    ):
        self.raw_args = raw_args
        self.data = data
        self.form_fields = form_fields

        # if the user renames the script file or the
        # web client, use their new names
        self.program_name = os.path.split(program_name)[-1]

        # flags that indicate origin of input
        self.web_form = web_form
        self.rpc = rpc

        self.option_parser = options.getParser()
        self.options = dict(common.settings)

        # data obtained from the proper source go here
        self.data_string = None

    def version_text(self) -> str:
        """
        print the program version

        :return: version text
        """
        return common.version_text(program_name=self.program_name)

    def help_text(self) -> str:
        """
        error messages for the command line interface.

        :return: help text
        """
        return common.help_text(program_name=self.program_name)

    def parseInputCli(self) -> None:
        """
        parse input that came through the command line (locally or rpc)
        return success flag and either error message or data

        :return: None
        """
        # catch empty input
        if not self.raw_args and not self.data:
            ht = self.help_text()

            raise HelpError(ht)

        # parse options and arguments
        try:
            parsed_options, data_list = self.option_parser.process_cli(self.raw_args)
        except Exception as msg:
            if str(msg).endswith("not recognized"):  # get opt error
                msg = f"{str(msg)}. Try {self.program_name} --help to see a list of available options."
            raise HelpError(msg)

        # if we get here, we have parsed options and a possibly empty data list
        self.options.update(parsed_options)

        # before we go on to check on the data, we will satisfy help requests,
        # which we treat like an error
        if self.options["help"]:
            raise HelpError(self.help_text())
        elif self.options["version"]:
            raise HelpError(self.version_text())

        if self.data is not None:
            data_list.append(self.data)

        # at this point, we should have reached the same state
        # by rpc and local invocation

        if len(data_list) != 1:
            if not data_list:
                raise common.MCFError("No input data supplied")
            raise common.MCFError("Please give only one file or data string as input")

        data = data_list[0]

        if not self.rpc and self.options["input"] == "file":
            try:
                with open(data, mode="r", encoding="utf-8") as fh:
                    data = fh.read()
            except IOError:
                raise common.MCFError(f"Can't read file {data}")

        self.data_string = data

    def parseInputWeb(self) -> None:
        """
        parse options and provide data provided through the web form

        :return: None
        """
        parsed_options, warnings = self.option_parser.process_form_fields(
            self.form_fields
        )

        if warnings:
            raise common.MCFError("<br/>\n".join(warnings))

        # no warnings ...
        self.options.update(parsed_options)
        self.data_string = self.data

    def process(self) -> molecule.Molecule:
        """
        process input from both web form and CLI

        :return: a molecule
        """
        if not self.web_form:
            self.parseInputCli()
        else:
            self.parseInputWeb()
        # let toolkit parse the molecule, and process it
        tk_mol = self.parseMolecule()

        # we now know how to deal with orphan atoms.
        # atoms, bonds = tkmol.countAtoms(), tkmol.countBonds()
        # if atoms <= 1 or bonds == 0:
        #   raise common.MCFError, "Input contains no bonds---can't render structure"

        mol = molecule.Molecule(self.options, tk_mol)

        return mol

    def parseMolecule(self) -> IndigoObject:
        """
        turn the input into a toolkit molecule according to user settings

        indigo is supposed to read transparently, so we can do away with
        the format setting, basically. If it's numeric, we ask pubchem;
        if it isn't, we consider it a molecule.

        :return: IndigoObject
        """
        raw_input = self.data_string

        try:
            pubchem_id = int(raw_input)
        except ValueError:
            pubchem_id = None

        if pubchem_id is not None:
            try:
                url = common.pubchem_url % pubchem_id
                pubchem_content = request.urlopen(url).read()
            except IOError:
                raise common.MCFError("No connection to PubChem")

            self.data_string = pubchem_content.decode()

        try:
            tkmol = Indigo().loadMolecule(self.data_string)
        except IndigoException:
            raise common.MCFError("Invalid input data")

        hydrogens = self.options["hydrogens"]

        if hydrogens == "add":
            tkmol.unfoldHydrogens()
            tkmol.layout()  # needed to give coordinates to added Hs

        elif hydrogens == "delete":
            tkmol.foldHydrogens()

        if not tkmol.hasCoord() or self.options["recalculate_coordinates"]:
            tkmol.layout()

        return tkmol


def process(
    raw_args: Union[List, str, None] = None,
    data: any = None,
    form_fields: any = None,
    program_name: str = "mol2chemfigPy3",
    web_form: bool = False,
    rpc: bool = False,
    inline: bool = False,
) -> Tuple[bool, Union[str, molecule.Molecule]]:
    """
    process is a convenience wrapper for external callers

    :param raw_args: arguments
    :param data: data
    :param form_fields: form fields
    :param program_name: program name
    :param web_form: whether is web form
    :param rpc: rpc
    :param inline: inline mode: if true return the raw result else the decorated result
    :return: (bool, molecule)
    """
    p = Processor(raw_args, data, form_fields, program_name, web_form, rpc)

    try:
        mol = p.process()

    except HelpError as msg:
        return False, str(msg)

    except common.MCFError:  # anticipated error - brief message enough
        msg = traceback.format_exc().splitlines()[-1]
        msg = msg.split(": ")[-1]
        return False, msg if inline else f"\033[0;31m{msg}\033[0m"

    except Exception:  # unexpected error - get full traceback
        tb = traceback.format_exc()
        return False, tb

    return True, mol
