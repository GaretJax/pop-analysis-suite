"""
Local and remote shell commands execution.

These functions are mainly wrappers around those found in the fabric library.
"""


from pas.conf import settings
from pas.conf import all_hosts

# pylint: disable-msg=W0611
# Disable warning about unused imports, as they are intended to be available
# directly from the shell module to avoid specific fabric imports

from fabric import state
from fabric.context_managers import settings as _context
from fabric.context_managers import hide as _hide
from fabric.context_managers import _setenv
from fabric.context_managers import nested as _nested
from fabric.context_managers import cd
from fabric.contrib.console import confirm
from fabric.operations import local as _local
from fabric.operations import run as _run
from fabric.operations import sudo as _sudo
from fabric.operations import prompt

# pylint: enable-msg=W0611


__all__ = [
    # shell module functions
    'ignore_warnings', 'workon', 'local', 'remote',
    
    # imported from the fabric library for external use
    'cd', 'prompt', 'confirm',
]


def ignore_warnings():
    """
    Returns a fabric context manager configured to silently ignore all
    warnings about running commands.
    """
    return _context(_hide('warnings'), warn_only=True)


def workon(hosts):
    """
    Returns a fabric context manager which sets the hosts list to the given
    list.
    
    If the passed hosts argument is a single string, it is silently converted
    to a list before.
    """
    if isinstance(hosts, basestring):
        hosts = [hosts]
    
    return _nested(_setenv(hosts=hosts))


def local(cmd):
    """
    Executes a local command without capturing and returning the output.
    
    Thin wraper around the fabric.operations.local function
    """
    return _local(cmd, capture=False)


def remote(cmd, pty=False, user=None, sudo=False):
    """
    Executes the given remote command on the hosts list set in the current
    context.
    
    If user is given or sudo evaluates to True, then a fabric.operations.sudo
    call is made, otherwise a simple fabric.operations.run.
    """
    if state.env.cwd:
        cmd = 'cd {0} && {1}'.format(state.env.cwd, cmd)
    
    with _context(user=settings.VM_USER, password=settings.VM_PASSWORD):
        for host in state.env.hosts or all_hosts():
            with _context(host_string=host):
                if user or sudo:
                    _sudo(cmd, user=user, pty=pty)
                else:
                    _run(cmd, pty=pty)


