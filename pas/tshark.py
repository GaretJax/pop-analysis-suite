"""
Various utilities to deal with remote tshark operations with support for
features such as background execution, stop on request, and advanced tshark
interactions.

Note that all of the commands which operate on remote hosts, respect the
current set context to retrieve the host lists. When this list is not set or
is empty, the command will be run on all hosts. Refer to the documentation on
pas.shell to obtain further information.

Most of the command below use the tshark command-line tool directly; refer to
its man page for the details about the usage.
"""


from pas import shell


def start(name, iface="lo", outfile="-", capture_filter=""):
    """
    Starts a new tshark capture in background using a named screen session.
    
    The name of the spawned screen session will be the provided name joined
    with the interface by a dot.
    """
    
    # tshark command, see `man tshark` for further information about the
    # capture_filter syntax
    tshark = 'tshark -i {iface} -t e -w {outfile} {filter}'.format(
        iface=iface,
        outfile=outfile,
        filter=capture_filter
    )
    
    # Execute the tshark command inside a named screen session to allow
    # execution in background and selective termination
    screen = 'screen -dmS {name}.{iface} {command}'.format(
        name=name,
        iface=iface,
        command=tshark
    )
    
    shell.remote(screen, sudo=True)


def stop(name, interface):
    """
    Stops the named tshark capture session on the given interface.
    
    The final name passed to the screen command will be the name joined with
    the interface by a dot.
    """
    shell.remote('screen -X -S {}.{} quit'.format(name, interface), sudo=True)


def kill():
    """
    Kills ALL running measures on the hosts provided by the context or
    (by default) on all known hosts.
    """
    with shell.ignore_warnings():
        shell.remote('pkill "tshark"', sudo=True)


def pcaptoxml(infile, outfile, display_filter=""):
    """
    Converts the pcap input file to XML and writes the output to outfile while
    filtering using the given display filter.
    
    Refer directly to the tshark man page for further informations about the
    display filter syntax.
    """
    shell.remote('tshark -T pdml -r {infile} -t e {filter} >{outfile}'.format(
        infile=infile,
        outfile=outfile,
        filter=display_filter
    ))

