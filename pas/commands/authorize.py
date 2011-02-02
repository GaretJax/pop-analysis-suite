"""
``pas authorize``
=================

**Usage:** ``pas authorize [-h]``

optional arguments:
  -h, --help  Show this help message and exit.


Exchanges the public keys between all VMs and adds each host to the
:file:`known_hosts` file of each other, in order to allow direct ssh
connections between VMs without need for external input.

This command operates only on the default ``rsa`` key and uses the shared
configuration directory to keep a temporary list of all public keys.

The function to which this command is bound doesn't need (and doesn't provide)
any specific command-line options and can thus be called in normal library
usage without any argument, like in the following example::

    from pas.commands.authorize import command as authorize

    authorize()

"""

import os

from pas import shell
from pas.conf import settings


def command(_=None):
    """
    Exchanges the public keys between all VMs to allow direct ssh connections
    between them without user input.
    """
    local, remote = settings.PATHS['configuration']
    local = os.path.join(local, 'authorized_keys')
    remote = os.path.join(remote, 'authorized_keys')

    with shell.ignore_warnings():
        shell.local('rm {0}'.format(local))

    # Collect all keys in one file
    shell.remote('cat $HOME/.ssh/id_rsa.pub >>{0}'.format(remote))

    # Copy first authorized key (host machine) to temp location
    shell.remote('head -1 $HOME/.ssh/authorized_keys ' \
                 '>$HOME/.ssh/authorized_keys.tmp')

    # Append all other keys
    shell.remote('cat {0} >>$HOME/.ssh/authorized_keys.tmp'.format(remote))

    # Move to the original location
    shell.remote('mv $HOME/.ssh/authorized_keys.tmp ' \
                 '$HOME/.ssh/authorized_keys')

    # Add all hosts to the known_hosts file
    shell.remote('cat $HOME/.ssh/authorized_keys | '\
                 'awk -F \' \' \'{print $3}\' | ' \
                 'grep -E \'[0-9.]{7,15}\' | ' \
                 'ssh-keyscan -f - -H -t rsa >$HOME/.ssh/known_hosts')

    shell.local('rm {0}'.format(local))

