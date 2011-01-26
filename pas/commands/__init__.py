"""
Support for a plug-in commands infrastructure.

Each command is a separate module in this package (pas.commands) and should at
least contain a command function (modules starting with an underscore will be
ignored).

The command function takes one required positional argument: an
argparse.Namespace instance with the parsed command line with which the
command was invoked.

The name of the command will be the same as the name of the module containing
the command function.

To add command-specific arguments to a given command, a getparser function
can be defined in the command module. This function takes an
argparse.SubParser instance and can freely customize it, the only setted
options are the command name and the command function.

This subparser will not be modified after the getparse call, so you can
imagine to do all weird things there in; just remember that for each run, all
getparser functions will be called and this can induce in some overhead when
there are many commands or when the getparse function executes slow or
long-lasting operations.
"""


import argparse
import imp
import functools
import logging
import os
import sys

from pas import VERSION
from pas import case
from pas import measure


def nosettings(func):
    """
    Normally the command invoker will try to load the settings and terminate
    the execution if no settings can be loaded, but some commands don't need
    the settings module and are specifically crafted to operate outside of an
    active suite.

    To instruct the invoker not to try to load the settings, a nosettings
    attribute with a non-fale value can be set on the command function; this
    decorator does exactly this.
    """
    func.nosettings = True
    return func


def select_case(func):
    """
    Wraps the given command and provides it with a valid test case, by asking
    the user to correct his input if necessary or by directly coercing to a
    valid value if possible.
    """
    @functools.wraps(func)
    def check_and_ask(options):
        """
        Modifies the case attribute of the passed argparse.Namespace instance
        to be a valid test case.
        """
        options.case = case.select(getattr(options, 'case', None))
        return func(options)

    return check_and_ask


def select_measure(func):
    """
    Wraps the given command and provides it with a valid measure, by asking
    the user to correct his input if necessary or by directly coercing to a
    valid value if possible.
    """
    @functools.wraps(func)
    def check_and_ask(options):
        """
        Modifies the measure attribute of the passed argparse.Namespace
        instance to be a valid measure.
        """
        options.measure = measure.select(getattr(options, 'measure', None))
        return func(options)

    return check_and_ask


def host_option(parser, argument=False):
    """
    Adds an optional --hosts option to the given parser which always returns a
    list of the hosts specified on the command line or an empty list if no
    hosts were specified.
    
    If the optional argument flag is set to true, then adds an argument insted
    of an option.

    Multiple hosts can be specified
    """
    if argument:
        help = ""
        parser.add_argument(
            'hosts',
            metavar='host',
            default=[],
            help=help,
            nargs='*'
        )
    else:
        help = ""
        parser.add_argument(
            '--host',
            metavar='HOST',
            dest='hosts',
            default=[],
            help=help,
            action='append'
        )


def case_argument(parser):
    """
    Adds an optional test case argument to the given parser.

    No validations are done on the parsed value as the settings have to be
    loaded to obtain the local test-cases path and they can't be loaded before
    the full command-line parsing process is completed.

    To bypass this issue, a select_case command decorator is provided which
    looks at the argparse.Namespace instance and does all the necessary steps
    to provide the commad with a valid test case path.
    """
    parser.add_argument('case', metavar='test-case', nargs='?')


def measure_argument(parser):
    """
    Adds an optional measure argument to the given parser.

    No validations are done on the parsed value as the settings have to be
    loaded to obtain the local shared-measures path and they can't be loaded
    before the full command-line parsing process is completed.

    To bypass this issue, a select_measure command decorator is provided which
    looks at the argparse.Namespace instance and does all the necessary steps
    to provide the commad with a valid measure path.
    """
    parser.add_argument('measure', nargs='?')


def case_or_measure_argument(parser):
    """
    Adds an optional argument represening either a case or a measure.

    Refer to the two specific functions documentation (case_argument and
    measure_argument) for further information.
    """
    parser.add_argument('case_or_measure', nargs='?')


def getdoc(obj):
    """
    Gets and formats an object docstring by keeping only the first paragraph
    (considering paragraphs separated by an empty line), removing the
    indentiation and merging multiple lines together.

    If the object had no docstring attached, an empty string will be returned.
    """
    docstring = obj.__doc__

    if not docstring:
        return ''

    # Convert tabs to spaces (following the normal Python rules)
    # and split into a list of lines
    lines = docstring.expandtabs().splitlines()

    # Determine minimum indentation (first line doesn't count)
    indent = sys.maxint
    for line in lines[1:]:
        stripped = line.lstrip()
        if stripped:
            indent = min(indent, len(line) - len(stripped))

    # Remove indentation (first line is special)
    trimmed = [lines[0].strip()]
    if indent < sys.maxint:
        for line in lines[1:]:
            trimmed.append(line[indent:].rstrip())

    # Strip off trailing and leading blank lines
    while trimmed and not trimmed[-1]:
        trimmed.pop()

    while trimmed and not trimmed[0]:
        trimmed.pop(0)

    # Get the full docstring
    fulldoc = '\n'.join(trimmed)

    # Split into paragraphs
    paragraphs = fulldoc.split('\n\n')

    # Return only the first paragraph (joined together)
    return paragraphs[0].replace('\n', ' ')


def settingspath(path):
    """
    Validator function to be used in the parser.add_argumet call for the
    settings module path.

    The retuned path is the realpath of the argument if it points to a
    directory and the dirname of the realpath of the argument if it end with
    a .py extension.

    This means that both the full path to the settings.py (or settings
    package, or settings compiled python .pyc) file/directory or to its
    containing directory can be specified and will be accepted.

    Note that no checks about the real existence of the settings module are
    done here.
    """
    path = os.path.realpath(path)

    # Take the containing directory if the path points directly to the module
    if path.endswith(('settings.py', 'settings.pyc', 'settings')):
        return os.path.dirname(path)

    return path


def load_package_subcommands(subparsers, package):
    log = logging.getLogger('pas.commands_builder')
    directory = os.path.dirname(package.__file__)

    for cmd in os.listdir(directory):
        path = os.path.join(directory, cmd)

        if cmd.startswith('_'):
            continue

        if not cmd.endswith('.py') and not os.path.isdir(path):
            continue

        name = cmd.rsplit('.', 1)[0]
        fullname = '{0}.{1}'.format(package.__name__, name)

        if cmd.endswith('.py'):
            # ...import the command and getparser function...
            module = imp.load_source(fullname, path)

            name = module.__name__.rsplit('.', 1)[-1]
            
            try:
                command = module.command
            except AttributeError:
                log = logging.getLogger('pas.commands_builder')
                log.error("No command found in module {}".format(module.__name__))
            else:
                subparser = subparsers.add_parser(name, help=getdoc(module))
                subparser.set_defaults(execute=command)
                if hasattr(module, 'getparser'):
                    module.getparser(subparser)
        else:
            # Recursively load the subpackage
            module = imp.load_source(fullname, os.path.join(path, '__init__.py'))

            name = module.__name__.rsplit('.', 1)[-1]
            subparser = subparsers.add_parser(name, help=getdoc(module))
            load_package_subcommands(subparser.add_subparsers(), module)


def build_parser():
    """
    Builds the complete command-line parser for the pas program by asking each
    command module inside the pas.commands package for subparser customization
    as described in the package docstring.
    """
    log = logging.getLogger('pas.commands_builder')

    # Get default path to the settings module
    settings = os.getenv('PAS_SETTINGS_MODULE') or os.getcwd()

    # Build main parser
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', action='version',
                        version='%(prog)s ' + VERSION)
    parser.add_argument('-v', '--verbose', default=list(),
                        action='append_const', const=1)
    parser.add_argument('-q', '--quiet', default=list(),
                        action='append_const', const=True)
    parser.add_argument('--settings', default=settings,
                        metavar='SETTINGS_MODULE', type=settingspath)

    # For each module/package in the pas.commands package...
    subparsers = parser.add_subparsers()
    load_package_subcommands(subparsers, sys.modules[__name__])
    
    dirs = ('commands', )
    
    for d in dirs:
        log.debug("Scanning external directory '{0}' for commands...".format(d))
        module = os.path.basename(d)
        c = imp.load_source(module, os.path.join(d, '__init__.py'))
        load_package_subcommands(subparsers, c)

    return parser


