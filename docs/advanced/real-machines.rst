Running ``pas`` with real machines
==================================

The ``pas`` tool was originally conceived to be run on a especially configured
VM setup, but it is enough flexible to be able to work on any machine if some
requirements are satisfied.

This section deals with the different assumptions the ``pas`` tool makes about
the guest machine and described how a real machine has to be set up in order
to be compatible with ``pas``.


Authentication
--------------

All communication between ``pas`` and the remote host happens through ``ssh``.
As the VMs are especially created for the measures, they don't have strict
security requirements and so password based authentication is used to connect
to them.

Furthermore ``pas`` assumes that all remote machines share the same username
and password.

To configure a real machine to be able to authenticate the ``pas`` tool, two
ways are possible:

 a. Configure the local host and the remote machine in order to authenticate
    themselves without user interaction (this is often done by using
    ``publickey`` authentication, but other, less secure, methods exist).

    The ``ssh`` transport layer will always try ``publickey`` authentication
    first thus different keys can be exchanged between different hosts and a
    good security level can be achieved.

 b. Create a user for ``pas`` on each machine giving it the same username and
    password and set the :data:`VM_USER <pas.conf.basesettings.VM_USER>` and
    the :data:`VM_PASSWORD <pas.conf.basesettings.VM_PASSWORD>` directives
    accordingly.

Furthermore, ``pas`` requires ``sudo`` permissions to execute certain commands.
On the default VM configurations, it does not need any password to execute
commands as root and the real machines have to be configured to behave the same
way.

The commands for which ``pas`` requires ``sudo`` privileges are to start, stop
and kill the ``jobmgr`` and ``tshark`` processes and to copy and delete the
files created by these.


Dependencies
------------

When using the default VMs, vagrant automatically sets them up to conform to
the ``pas`` requirements. You can directly use the chef configuration bundled
with each environment or manually set up your machines to conform to these
requirements.

The following packages are required by ``pas``:

 * A ``popc`` installation, configured in accordance with the role assigned to
   the machine.

 * The ``tshark`` executable, often provided by the system package manager.
 
 * The ``screen`` executable, often provided by the system package manager, if
   not already installed.

 * A ``getip`` shell script available on the path which prints the IP address
   of the interface given as its only argument.


Shared folders
--------------

Vagrant allows to easily set up shared folders between the host and one or more
guest operating systems. ``pas`` builds upon this feature to be able to
distribute the source code and recover the measure results. 

The following folders on the remote hosts have to be shared with the local
host:

 * ``/share/test-cases`` on the remote host has to be mapped to the ``cases``
   directory of the test environment.

 * ``/share/measures`` on the remote host has to be mapped to the ``reports``
   directory of the test environment.

 * ``/share/conf`` on the remote host has to be mapped to the ``conf``
   directory of the test environment.

.. note::
   These paths can be configured using the :data:`PATHS
   <pas.conf.basesettings.PATHS>` setting directive.
   
   This means that you can adjust these paths to your liking as long as there
   are three shared folders between the systems and that the settings file is
   configured accordingly.

.. note::
   If sharing folders is not an option, you can always build custom subcommands
   to override the commands which need shared folders and do the file transfers
   over ssh using ``scp`` or with ``rsync``.



