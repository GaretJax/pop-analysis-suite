"""
``pas`` provides a set of default configuration directives (explained in detail
below). All of these settings can be modified (and new directives added) by
overriding them in the environment-specific ``settings.py`` file.

The ``pas`` command line tool automatically loads these directives at startup
and then, once read the ``--settings`` command line options, will load the
environment-specific settings file letting it override the already defined
values or adding new ones (for example for your :ref:`command-subsystem`).

The syntax of the settings file is simple: each uppercase public (not starting
with an underscore) member is set as an attribute of the global ``Settings``
object.
"""


# Please don't alter the values inside this file, as these can be customized
# and overridden in the environment level settings module.


VM_USER = 'vagrant'
"""
Username to use to connect to a remote machine through ``ssh``.
"""

VM_PASSWORD = 'vagrant'
"""
Password to use to connect to a remote machine through ``ssh``, is only used
if ``publickey`` authentication is not available or if it fails.
"""

ROLES = {
    'master': [],
    'client': [],
    'slaves': [],
}
"""
A mapping of role names to IP addresses. The roles are defined as follows:

master
   Guest machines running a jobmgr instance configured as a master node. The
   job managers on these machines are started before and stopped after the job
   managers on slave machines.
   
   Normally these machines run a job manager configured with 0 available object
   slots, in order to delegate parallel objects execution to slaves.
  
slaves
   Guest machines running a jobmgr instance configured as a slave node. The job
   managers on these machines are started after and stopped before the job
   managers on master machines.
   
client
   Machines on which the measure case if first started.
  
.. note::
   An IP address can appear more than one time in different roles. For example,
   a master node can also be a client (this is the default for newly created
   environments).
"""

INTERFACES = {
    'master': ['eth1', 'lo'],
    'slaves': ['lo'],
    'client': [],
}
"""
A mapping of role names to interfaces. A measure will be started for each
interface of each machine of a given role. The :func:`pas.conf.map_interfaces`
function provides an easy way to create a list of
(``hostname``, ``interfaces``) tuples.
"""

CAPTURE_FILTER = "'tcp and not tcp port 22'"
"""
Capture filter to use with the ``tshark`` command line tool when running a new
measure. Note that this is different from the display filter directive (and
also uses a different syntax).

The `capture filters <http://wiki.wireshark.org/CaptureFilters>`_ page on the
wireshark wiki provides more informations about this specific syntax.

The default filter captures all TCP traffic excluding ``ssh`` connections on
the default port (22).
"""

DISPLAY_FILTER = "'" + ' || '.join((
    "tcp.flags.syn == 1",
    "tcp.flags.push == 1",
    "tcp.flags.fin == 1",
    "tcp.flags.ack == 1"
)) + "'"
"""
Display filters to use with the ``tshark`` command line tool when converting
the measures to xml. Note that this is different from the capture filter
directive (and also uses a different syntax).

The `display filters <http://wiki.wireshark.org/DisplayFilters>`_ page on the
wireshark wiki provides more informations about this specific syntax.

The default filter actually does not filter anything (all non tcp traffic is
already filtered out by the capture filter) but provides a good starting point
for advanced tcp filtering.

.. note::
   It is considered good practice to move as much filtering as possible to the
   capture phase. Sadly the capture filters don't offer the powerful filtering
   expressions which are indeed possible using the display filters syntax.
"""

LOG_FILES = (
    '/tmp/jobmgr_stdout_*',
    '/tmp/jobmgr_stderr_*',
    '/tmp/paroc_service_log',
    '/tmp/popc_node_log',
)
"""
List of path to log files on the remote host which have to be copied along with
the measures during the collect phase.

The paths are copied using a simple ``cp`` command, it is thus possible to
use shell variables and substitutions pattern therein.

.. note::
   The :py:mod:`pas.commands.jobmgr.start` command deletes these files each
   time it is executed.
"""

PATHS = {
    'test-cases':      ['cases',   '/share/test-cases'],
    'configuration':   ['conf',    '/share/conf'],
    'local-measures':  [None,      '/measures'],
    'shared-measures': ['reports', '/share/measures'],
}
"""
General path configuration. Contains a mapping between symbolic path name (i.e.
``test-cases``) to a tuple of its local (i.e. ``cases``) and remote (i.e.
``/share/test-cases``) equivalent.

With the exception of the ``local-meaures`` entry, these path are all shared
using the ``Vagrantfile`` ``config.vm.share_folder`` directive.

.. note::
   This settings directive is available mainly to centralize the path
   configuration and is not meant to be modified. Override these values only
   if you are sure of what you are doing.
"""

STARTUP_DELAY = 2
"""
Delay to introduce between master ``jobmgr`` startup and slave ``jobmgr``
startup, in seconds.
"""

SHUTDOWN_DELAY = 2
"""
Delay to introduce between slave ``jobmgr`` shutdown and master ``jobmgr``
shutdown, in seconds.
"""

COMMAND_DIRECTORIES = (
    'commands',
)
"""
List of external directories to scan for additional commands. Refer to the
:ref:`command-subsystem` document for more information about the creation and
use of custom commands.
"""

