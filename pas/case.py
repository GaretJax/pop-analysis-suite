"""
Collection of utilities to deal with the management of the different test
cases of the suite.
"""


import os

from pas import shell
from pas.conf import settings
from pas.conf import all_hosts
from pas.conf import role


def select(name=None, basedir=None):
    """
    Scans the basedir (or the test-cases directory defined in the settings)
    for directories and returns a choice based on different criteria:

     1. No directories are found; raise a RuntimeError
     2. The name is set; check if it was found and if so return it
     3. Only one directory is found; return the found directory
     4. Multiple directories are found; ask the user to pick one
     
     
     a. If no measure case exist yet, a ``RuntimeError`` is thrown;
     b. If only one measure case is found, its path is returned;
     c. If more than one measure cases are found, then the user is asked to
        choose one between them.

     The list presented to the user when asked to choose a case will be
     something like the following::

         Multiple test cases found:

              [0]: simple
              [1]: complex

         Select a test case: _
    """

    if not basedir:
        basedir = settings.paths['test-cases'][0]

    # Get all files in the directory
    paths = os.listdir(basedir)

    # Rebuild the full path name
    paths = [(os.path.join(basedir, p), p) for p in paths]

    # Filter out non-directories
    paths = [p for p in paths if os.path.isdir(p[0])]

    # If no entries remained, there are no test cases which can be run
    if not paths:
        raise RuntimeError("No test cases found.")

    # Check to see if chosen value exists in the available paths
    if name:
        for path in paths:
            if path[1] == name:
                return path
        else:
            # Continue with selecting phase
            # @TODO: log
            print "The chosen path is not available."

    # There is not much to choose here
    if len(paths) == 1:
        # @TODO: log
        print "\nOnly one test case found: {0}.".format(paths[0][1])
        return paths[0]

    # Present a list of choices to the user (paths must now contain more than
    # one item)
    print "\nMultiple test cases found:\n"

    for i, (path, name) in enumerate(paths):
        index = '[{0}]'.format(i)
        print '{0:>8s}: {1}'.format(index, name)

    def valid(index):
        """
        Returns the correct entry in the paths list or asks for a correct
        value if the index is outside the boundaries.
        """
        try:
            return paths[int(index)]
        except (IndexError, ValueError):
            raise Exception("Enter an integer between 0 " \
                            "and {0}.".format(len(paths)-1))

    print
    return shell.prompt("Select a test case:", validate=valid)


# pylint: disable-msg=W0622
# Disable warnings for the overriding of the built in compile function.
# Who is using it, anyway...

def compile(name, localdir=None, remotedir=None):
    """
    Compiles the given test case on all the hosts in the system.

    The building details and the respect of the convention are enforced by the
    Makefile and not further explained here.
    """
    # Read the defaults from the settings if the arguments are not provided
    if not localdir or not remotedir:
        paths = settings.paths['test-cases']

        if not localdir:
            localdir = paths[0]

        if not remotedir:
            remotedir = paths[1]

    local = os.path.join(localdir, name)
    remote = os.path.join(remotedir, name)

    with shell.ignore_warnings():
        shell.local('rm {0}/build/obj.map'.format(local))

    with shell.workon(all_hosts()):
        with shell.cd(remote):
            shell.remote('make clean && make')


def execute(name, remotedir=None):
    """
    Executes the given test case on all client hosts (normally onle one).
    """
    if not remotedir:
        remotedir = settings.paths['test-cases'][1]

    remote = os.path.join(remotedir, name)

    with shell.workon(role('client')):
        with shell.cd(remote):
            shell.remote('make run', pty=True)


