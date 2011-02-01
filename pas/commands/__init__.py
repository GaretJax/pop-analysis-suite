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
    Instructs the command dispatcher to not try to load the settings when
    executing this command.

    Normally the command invoker will try to load the settings and will
    terminate the execution if not able to do so, but some commands don't need
    the settings module and are specifically crafted to operate outside of an
    active testing environment.

    To instruct the invoker not to try to load the settings, a nosettings
    attribute with a non-false value can be set on the command function; this
    decorator does exactly this.

    You can use it like this::

        from pas.commands import nosettings

        @nosettings
        def command(options):
            # Do something without the settings
            pass

    :param func: The command function for which the settings don't have to be
                 loaded.
    """
    func.nosettings = True
    return func


def select_case(func):
    """
    Adds a ``case`` attribute to the ``Namespace`` instance passed to the
    command, containing a tuple of ``(full-path-on-disk-to-the-measure-case,
    measure-case-basename)``.

    The ``case`` attribute is populated by calling the
    :py:func:`pas.case.select` function.

    If a ``case`` attribute is already set on the ``Namespace`` its value will
    be passed to the the :py:func:`pas.case.select` function as default value
    for the selection.

    You can use it like this::

        from pas.commands import select_case

        @select_case
        def command(options):
            # Do something with the measure case
            print options.case

    :param func: The command function for which the a case has to be selected.
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
    Adds a ``measure`` attribute to the ``Namespace`` instance passed to the
    command, containing a tuple of ``(full-path-on-disk-to-the-measure,
    measure-basename)``.

    The ``measure`` attribute is populated by calling the
    :py:func:`pas.measure.select` function.

    If a ``measure`` attribute is already set on the ``Namespace`` its value
    will be passed to the the :py:func:`pas.measure.select` function as default
    value for the selection.

    You can use it like this::

        from pas.commands import select_measure

        @select_measure
        def command(options):
            # Do something with the measure
            print options.measure

    :param func: The command function for which the a case has to be selected.
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
    Adds an optional ``--host`` option to the ``parser`` argument.

    The given hosts can be read using the ``hosts`` attribute of the
    ``Namespace`` instance passed to the command to be executed.

    The resulting ``hosts`` attribute will always be a list of the hosts
    specified on the command line or an empty list if no hosts were specified.

    If the optional ``argument`` flag is set to true, then this decorators adds
    an argument insted of an option.

    Multiple hosts can be specified using multiple times the ``--host`` option
    or by giving multiple ``HOST`` arguments as appropriate.

    Use it like this::

        from pas.commands import host_option

        def getparser(parser):
            host_option(parser)

        def command(options):
            # Do something with it
            print options.hosts

    :param parser: The ``ArgumentParser`` instance on which the ``--host``
                   option shall be attached.
    :param argument: A flag indicating if the hosts shall be parsed as
                     arguments instead.
    """
    helpmsg = """Use this option to specify one or more hosts on which this
                 command has to be run."""

    if argument:
        parser.add_argument(
            'hosts',
            metavar='HOST',
            default=[],
            help=helpmsg,
            nargs='*'
        )
    else:
        helpmsg += """ The --host option can be specifed multiple times to
                      define multiple hosts."""

        parser.add_argument(
            '--host',
            metavar='HOST',
            dest='hosts',
            default=[],
            help=helpmsg,
            action='append'
        )


def case_argument(parser):
    """
    Adds an optional ``case`` argument to the given parser.

    No validations are done on the parsed value as the settings have to be
    loaded to obtain the local measure-cases path and they can't be loaded
    before the full command-line parsing process is completed.

    To bypass this issue, the :func:`pas.commands.select_case` command
    decorator can be used which looks at the ``Namespace`` instance and does all
    the necessary steps to provide the command with a valid measure case path.
    
    Use it like this::

        from pas.commands import case_argument, select_case

        def getparser(parser):
            case_argument(parser)

        @select_case   # Optional
        def command(options):
            # Do something with it
            print options.case

    :param parser: The ``ArgumentParser`` instance on which the ``case``
                   argument shall be attached.
    """
    parser.add_argument('case', metavar='MEASURE_CASE', nargs='?')


def measure_argument(parser):
    """
    Adds an optional ``measure`` argument to the given parser.

    No validations are done on the parsed value as the settings have to be
    loaded to obtain the local measures path and they can't be loaded before
    the full command-line parsing process is completed.

    To bypass this issue, the :func:`pas.commands.select_measure` command
    decorator can be used which looks at the ``Namespace`` instance and does all
    the necessary steps to provide the command with a valid measure path.
    
    Use it like this::

        from pas.commands import measure_argument, select_measure

        def getparser(parser):
            measure_argument(parser)

        @select_measure   # Optional
        def command(options):
            # Do something with it
            print options.measure

    :param parser: The ``ArgumentParser`` instance on which the ``measure``
                   argument shall be attached.
    """
    parser.add_argument('measure', metavar="MEASURE", nargs='?')


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

    # Return only the first paragraph (joined together)
    return "\n\n".join(p.replace('\n', ' ') for p in fulldoc.split('\n\n'))


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
    """
    Recursively loads all the subcommands contained in the given package as
    subparsers for the given subparser.
    """
    
    # pylint: disable-msg=W0212
    # Disable warning for accessing the _actions member of the ArgumentParser
    # class.
    
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
                msg = "No command found in module {}".format(module.__name__)
                log.error(msg)
            else:
                subparser = subparsers.add_parser(name, help=getdoc(command))
                subparser._actions[0].help = "Show this help message and exit."
                subparser.set_defaults(execute=command)
                if hasattr(module, 'getparser'):
                    module.getparser(subparser)
        else:
            # Recursively load the subpackage
            path = os.path.join(path, '__init__.py')
            module = imp.load_source(fullname, path)

            name = module.__name__.rsplit('.', 1)[-1]
            subparser = subparsers.add_parser(name, help=getdoc(module))
            subparser._actions[0].help = "Show this help message and exit."
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
                        action='append_const', const=1, help="Increments the "\
                        "verbosity (can be used multiple times).")
    parser.add_argument('-q', '--quiet', default=list(),
                        action='append_const', const=1, help="Decrements the "\
                        "verbosity (can be used multiple times).")
    parser.add_argument('--settings', default=settings,
                        metavar='SETTINGS_MODULE', type=settingspath,
                        help="The path to the settings module")


    # pylint: disable-msg=W0212
    # Disable warning for accessing the _actions member of the ArgumentParser
    # class.
    parser._actions[0].help = "Show this help message and exit."
    parser._actions[1].help = "Show program's version number and exit."

    # For each module/package in the pas.commands package...
    subparsers = parser.add_subparsers()
    load_package_subcommands(subparsers, sys.modules[__name__])

    dirs = ()

    for d in dirs:
        log.debug("Scanning external directory '{0}' for commands...".format(d))
        module = os.path.basename(d)
        package = imp.load_source(module, os.path.join(d, '__init__.py'))
        load_package_subcommands(subparsers, package)

    return parser


