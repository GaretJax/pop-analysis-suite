#!/usr/bin/env python
"""
Main command line script of the pas package.

The main function contained in this module is used ai main entry point for the
pas command line utility.

The script is automatically created by setuptool, but this file can be
directly invoked with `python path/to/pas.py` or directly if its executable
flag is set.
"""


import logging
import logging.handlers
import os
import sys

# pylint: disable-msg=E0611
# I know relative imports are not the holy grail, but here we need them and
# it is a pylint bug not to recognized empty parent paths.

from .. import commands              # Relative imports to avoid name clashing
from ..conf import settings          # Relative imports to avoid name clashing

# pylint: enable-msg=E0611
# Reenable unknown name detection

from fabric.state import connections


# pylint: disable-msg=W0105
# Docstring for variables are not recognized by pylint, but epydoc parses them


LOGFILE = os.getenv('PAS_LOGFILE') or 'pas.log'
"""Logfile name, settable using the PAS_LOGFILE env variable"""


VERBOSITY = logging.INFO
"""Default verbosity for console output"""


def main():
    """
    First function called upon command line invocation. Builds the command
    line parser, parses the arguments, configures logging and invokes the
    command.
    """

    # Build parser
    parser = commands.build_parser()

    # Parse arguments
    command = args = parser.parse_args()

    # Get the verbosity level
    verbosity = max(1, VERBOSITY - 10 * (len(args.verbose) - len(args.quiet)))

    # Configure logging
    file_formatter = logging.Formatter("%(asctime)s - %(levelname)10s - " \
                                       "%(message)s (%(pathname)s:%(lineno)d)")

    # All console output not explicitly directed to the user should be a log
    # message instead
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(verbosity)

    # Buffer the logging until no errors happen
    buffered_handler = logging.handlers.MemoryHandler(9999, logging.CRITICAL)
    
    # Capture all logging output and write it to the specified log file
    file_handler = logging.FileHandler('pas.log', 'w', delay=True)
    file_handler.setFormatter(file_formatter)
    buffered_handler.setTarget(file_handler)

    logger = logging.getLogger()
    logger.setLevel(1)
    logger.addHandler(console_handler)
    logger.addHandler(buffered_handler)
    
    paramiko_logger = logging.getLogger('paramiko.transport')
    paramiko_logger.setLevel(verbosity + 10)

    res = 0

    # Load settings if needed
    if not getattr(command.execute, 'nosettings', False):
        try:
            settings.loadfrompath(path=args.settings)
        except ImportError:
            res = 1

    # Execute command
    if not res:
        res = command.execute(args)

        # Cleanup fabric connections if needed
        for key in connections.keys():
            connections[key].close()
            del connections[key]
    
    # Check execution result
    if res:
        # ...an error occurred, write the logfile
        buffered_handler.flush()
        print
        print "pas exited with a non-zero exit status (%d). A complete log " \
              "was stored in the %s file." % (res, LOGFILE)
        print
    else:
        # ...no errors occurred, avoid to flush the buffer
        buffered_handler.setTarget(None)
    
    # Need to close the buffered handler before sysexit is called or it will
    # result in an exception
    buffered_handler.close()
    
    return res


if __name__ == '__main__':
    sys.exit(main())

