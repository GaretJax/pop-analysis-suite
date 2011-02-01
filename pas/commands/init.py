"""
``pas init``
===============

**Usage:** ``pas init [-h] [DIR]``

positional arguments:
   .. cmdoption:: DIR

      The directory inside which the environment shall be created.

optional arguments:
  -h, --help   show this help message and exit

Sets up a new measurement and analysis environment in the selected directory
(or in the CWD if none is provided).

The directory has to be empty or inexistent. The command will fail if the
directory already exists and is non-empty.

The environment is mainly set up by recursively copying all the files inside
pas.conf.suite_template to the newly created directory.
"""


import os
import logging

from pas import env
from pas import commands


# pylint: disable-msg=C0111
# Disable warning for the missing docstrings, there is not much to document
# here. For further information refer directly to the enclosed called function
# documentation.


def getparser(parser):
    parser.add_argument('dir', metavar="DIR", nargs='?', default='.', type=str,
                        help='The directory inside which the environment ' \
                             'shall be created')

@commands.nosettings
def command(options):
    """
    Sets up a new measurement and analysis environment in the selected directory
    (or in the CWD if none is provided).
    """
    log = logging.getLogger('pas.commands')
    dest = os.path.realpath(options.dir)
    
    log.info("Attempting to create a new environment in '%s'...", dest)

    if os.path.exists(dest):
        # If the path already exists, make sure it is a directory and it is
        # empty.
        if not os.path.isdir(dest):
            log.critical("The selected path is not a directory.")
            return 1

        if os.listdir(dest):
            log.critical("The selected directory is not empty.")
            return 1
    else:
        # Create the directory
        try:
            os.mkdir(dest)
        except OSError as e:
            log.critical("An error occurred while creating the directory to" \
                         " host the environment (%s: %s).", e.errno, e.strerror)
            return 1
    
    env.setup(dest)

    log.info("Done.")

