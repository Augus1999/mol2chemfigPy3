# -*- coding: utf-8 -*-
"""
parsing options with a nicer wrapper around getopt.
Still throws getopt.GetoptError at runtime.

Let's try to combine this with basic html form
parsing, so that we can declare the options just
once.

Can we make this a bit more elegant by using
class attributes and more subclassing than
instantiation? The problem then is, of course,
that client code will have to do both.
"""
import getopt
import re
import textwrap


class OptionError(Exception):
    pass


class Option(object):
    collapseWs = re.compile('\s+')

    form_tag_template = "<!-- Option class needs to define a valid form tag template -->"

    def __init__(self,
                 long_name,
                 short_name,
                 form_text: any = None,
                 key: any = None,
                 default: any = None,
                 valid_range: any = None,
                 help_text: str = """
                 Our engineers deemed it self-explanatory
                 """):

        self.long_name = long_name
        self.short_name = short_name
        self.key = key or long_name
        self.form_text = form_text or long_name
        self.valid_range = valid_range  # must precede assignment of self.default

        if default is None:
            default = self._default()
        self.default = self.value = default

        self.help_text = help_text

    def _default(self) -> None:
        return None

    def validate_range(self, value) -> bool:
        """
        can be overridden if more general tests are needed
        """
        return self.valid_range is None or value in self.valid_range

    def validate(self, value) -> bool:
        success, converted = self._validate(value)
        success = success and self.validate_range(converted)

        if success:
            self.value = converted
            return True
        return False

    def validate_form_value(self, value) -> bool:
        """
        validation of option value received through a
        web form. May need to be different from CLI,
        but by default it's not.
        """
        return self.validate(value)

    def _validate(self, value) -> (bool, any):
        """
        no-op default
        """
        return True, value

    def short_getopt(self) -> str:
        """
        short option template for getopt
        """
        return self.short_name + ':'

    def long_getopt(self) -> str:
        """
        long option template for getopt
        """
        return self.long_name + '='

    def format_help(self, indent=30, linewidth=80) -> list:
        """
        format option and help text for console display
        maybe we can generalize this for html somehow
        """
        help_text = '%s (Default: %s)' % (self.help_text, self.default)
        help_text = self.collapseWs.sub(' ', help_text.strip())

        h_wrap = textwrap.wrap(help_text,
                               width=linewidth,
                               initial_indent=' ' * indent,
                               subsequent_indent=' ' * indent)

        opts = '-%s, --%s' % (self.short_name, self.long_name)
        h_wrap[0] = opts.ljust(indent) + h_wrap[0].lstrip()

        return h_wrap

    def format_tag_value(self, value) -> str:
        """
        format the default value for insertion into form tag
        """
        if value is None:
            return ''
        return str(value)

    def format_tag(self, value=None) -> (any, str, any, any):
        """
        render a html form tag
        """
        value = value or self.default

        values = dict(key=self.key, value=self.format_tag_value(value))
        tag = self.form_tag_template % values

        return self.key, tag, self.form_text, self.help_text


class BoolOption(Option):

    form_tag_template = r'''<input type="checkbox" name="%(key)s" value="yes" %(value)s/>'''

    def _default(self) -> bool:
        return False

    def validate(self, value=None) -> bool:
        """
        value should be empty; we accept and discard it.
        we simply switch the default value.
        """
        self.value = not self.default
        return True

    def validate_form_value(self, value) -> bool:
        """
        if a value arrives through a web form, the box has been
        ticked, so we set to True regardless of default. The passed
        value itself is unimportant.
        """
        self.value = True
        return True

    def short_getopt(self) -> str:
        return self.short_name

    def long_getopt(self) -> str:
        return self.long_name

    def format_tag_value(self, value) -> str:
        if value is True:
            return 'checked="checked"'
        else:
            return ''


class SelectOption(Option):
    """
    make a selection from a list of valid string values.
    argument valid_range cannot be empty with this class.
    """
    option_template = r'''<option value="%(option)s" %(selected)s>%(option)s</option>'''
    field_template = '''<select name="%(key)s">\n%(options)s\n</select>'''

    def _default(self) -> None:
        """
        we stipulate that valid_range is not empty.
        """
        try:
            return self.valid_range[0]
        except (TypeError, IndexError):
            raise OptionError('valid_range does not supply default')

    def _validate(self, value) -> (bool, str):
        """
        we enforce conversion to lowercase
        """
        return True, value.lower()

    def format_tag(self, value=None) -> (any, str, any, any):

        value = value or self.default

        options = []

        if not (self.default in self.valid_range):  # why am I doing this here?
            raise OptionError('invalid default')

        for option in self.valid_range:
            if option == value:
                selected = 'selected="selected"'
            else:
                selected = ''
            options.append(self.option_template % dict(option=option, selected=selected))

        option_string = '\n'.join(options)

        tag = self.field_template % dict(options=option_string, key=self.key)
        return self.key, tag, self.form_text, self.help_text


class TypeOption(Option):
    """
    coerces an input value to a type
    """
    _type = int
    _class_default = 0
    form_tag_template = r'''<input type="text" name="%(key)s" value="%(value)s" size="8"/>'''

    def _validate(self, value) -> (bool, any):
        try:
            converted = self._type(value)
            return True, converted
        except ValueError:
            return False, value


class IntOption(TypeOption):
    _type = int


class FloatOption(TypeOption):
    _type = float


class StringOption(TypeOption):
    _type = str


class RangeOption(Option):
    """
    accept a string that can be parsed into one or more int ranges,
    such as 5-6,7-19
    these should be converted into [(5,6),(7,19)]
    """
    outer_sep = ','
    inner_sep = '-'
    form_tag_template = r'''<input type="text" name="%(key)s" value="%(value)s" size="8"/>'''

    def _validate(self, rawvalue) -> (bool, list):
        ranges = []
        outer_frags = rawvalue.split(self.outer_sep)

        for frag in outer_frags:
            inner_frags = frag.split(self.inner_sep)
            if len(inner_frags) != 2:
                return False, rawvalue
            try:
                ranges.append((int(inner_frags[0]), int(inner_frags[1])))
            except ValueError:
                return False, rawvalue

        return True, ranges


class OptionParser(object):
    """
    collect and process options. the result will be contained in a dict.
    """
    def __init__(self) -> None:
        self._options = []
        self._options_by_name = {}
        self._options_by_key = {}

    def append(self, option) -> None:
        if option.short_name in self._options_by_name:
            raise OptionError("option name clash %s" % option.short_name)
        if option.long_name in self._options_by_name:
            raise OptionError("option name clash %s" % option.long_name)

        self._options_by_name[option.short_name] = option.key
        self._options_by_name[option.long_name] = option.key
        self._options_by_key[option.key] = option
        # also maintain options ordered in a list
        self._options.append(option)

    def validKeys(self) -> list:
        """
        required by the web form front end
        """
        return list(self._options_by_key.keys())

    def option_values(self) -> dict:
        """
        read current option values
        """
        option_dict = {}

        for option in self._options:
            option_dict[option.key] = option.value

        return option_dict

    def process_form_fields(self, fields) -> (dict, list):
        """
        process options received through the web form.
        we don't look at the cargo data here at all.

        what do we do about invalid options? puke? ignore?
        create a list of warnings and then ignore.
        """
        warnings = []

        for key, value in list(fields.items()):
            option = self._options_by_key[key]
            if not option.validate_form_value(value):
                msg = 'Invalid value %s for option %s ignored' % (value, option.form_text)
                warnings.append(msg)

        return self.option_values(), warnings

    def process_cli(self, rawinput) -> (dict, any):
        """
        process input from the command line interface
        - assemble template strings for getopt and run getopt
        - pass the result back to each option
        """
        try:  # accept lists or strings
            rawinput = rawinput.strip().split()
        except AttributeError:
            pass

        shorts, longs = self.format_for_getopt()

        opts, args = getopt.getopt(rawinput, shorts, longs)

        for opt_name, value in opts:
            key = self._options_by_name[opt_name.lstrip('-')]
            option = self._options_by_key[key]

            if not option.validate(value):
                msg = ["rejected value '%s' for option %s" % (value, opt_name), 'Option usage:']
                msg.extend(option.format_help())
                raise OptionError('\n'.join(msg))

        return self.option_values(), args

    def format_for_getopt(self) -> (str, list):
        shorts = ''.join([option.short_getopt() for option in self._options])
        longs = [option.long_getopt() for option in self._options]

        return shorts, longs

    def format_for_lua(self) -> str:
        """
        with lua, we use dumb option parsing. we only provide enough
        information for lua to distinguish between options with and
        without arguments.
        """
        bools = [opt for opt in self._options if isinstance(opt, BoolOption)]
        shorts = [nb.short_name for nb in bools]
        return ''.join(shorts)

    def format_help(self, indent=25, linewidth=70, separator=None) -> str:
        """
        just ask the options to render themselves
        """
        output = []

        for option in self._options:
            output.extend(option.format_help(indent, linewidth))

            if separator is not None:
                output.append(separator)

        return '\n'.join(output)

    def form_tags(self) -> list:
        """
        collect the html for each option
        """
        return [opt.format_tag() for opt in self._options]
