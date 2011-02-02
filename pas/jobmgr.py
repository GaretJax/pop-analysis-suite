"""
Remote JobMgr management utilities.

The following functions provide some wrappers around remote shell commands to
easily start, stop, restart or otherwise interact with a POP-C++ job manager.
"""


import time

from pas import shell
from pas.conf import role
from pas.conf import settings


def start():
    """
    Starts a JobMgr instance on one or more (depending on the current context)
    remote nodes.
    
    This function is intended to be used to start a single node. To start all
    nodes of a system, use the startall function, which introduces some delays
    to allow a correct registration of the slaves by the master.
    """
    # pty required to be set to true, otherwise the remote invocation hangs
    # and never returns
    shell.remote('SXXpopc start', pty=True, sudo=True)


def stop():
    """
    Stops a currently running JobMgr instance on one or more (depending on the
    current context) remote nodes.
    
    This function is intended to be used to stop a single node. To stop all
    nodes of a system, use the startall function, which introduces some delays
    to allow a correct registration of the slaves by the master.
    """
    shell.remote('SXXpopc stop', sudo=True)


def restart():
    """
    Stops and restarts a currently running JobMgr instance on one or more
    (depending on the current context) remote nodes in a unique command.
    
    This function is intended to be used to restart a single node. To restart
    all nodes of a system, use the startall function, which introduces some
    delays to allow a correct registration of the slaves by the master.
    """
    shell.remote('SXXpopc stop ; SXXpopc start', pty=True, sudo=True)


def kill():
    """
    Kills ALL running job managers (and the relative search nodes) on the
    hosts provided by the context or (by default) on all known hosts.
    """
    with shell.ignore_warnings():
        shell.remote('pkill "jobmgr|popc_*"', sudo=True)


def startall():
    """
    Starts all nodes of the system grouped by roles with the necessary delays
    to allow a proper registration to the parent JobMgr.
    
    The delay between the invocations can be set in the settings.
    """
    # Start all masters before, allowing for a proper setup before registering
    # a new slave
    with shell.workon(role('master')):
        start()

    # Wait some (configurable) time. One or two seconds should be enough here
    time.sleep(settings.STARTUP_DELAY)

    # And now start the slaves
    with shell.workon(role('slaves')):
        start()

    # Wait again some time for possible subsequent programs execution
    time.sleep(settings.STARTUP_DELAY)


def stopall():
    """
    Stops all nodes of the system grouped by roles with the necessary delays
    to allow a proper registration to the parent JobMgr.
    
    The delay between the invocations can be set in the settings.
    
    Note that in this case the delays are not as important as in the start 
    function on could probably safely be omitted. The behavior is preserved to
    grant compatibility with future versions of the JobMgr which possibly
    wants to execute some cleanup code before terminating.
    
    In the meanwhile it is possible to set the delay to 0 in the settings.
    """
    with shell.workon(role('slaves')):
        stop()

    time.sleep(settings.SHUTDOWN_DELAY)

    with shell.workon(role('master')):
        stop()

    time.sleep(settings.SHUTDOWN_DELAY)


def restartall():
    """
    Restarts all nodes in the system using the stopall and startall functions.
    
    Due to the introduction of the delays, the stop and start calls will not
    happen in the same command as for the restart function.
    """
    stopall()
    startall()


def killall():
    """
    Alias for the kill function, as no special treatment is needed here.
    """
    kill()

