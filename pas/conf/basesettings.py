"""
Base settings for any pas environment.

Please don't alter the values inside this file, as these can be customized and
overridden in the environment and test case level settings module.
"""

# pylint: disable=C0103

vm_user = 'vagrant'
vm_password = 'vagrant'

roles = {
    'master': ['33.33.33.10'],
    'client': ['33.33.33.10'],
    'slaves': ['33.33.33.11'],
}

interfaces = {
    'master': ['eth1', 'lo'],
    'slaves': ['lo'],
    'client': [],
}

capture_filter = "'tcp and not tcp port 22'"
display_filter = "'" + ' || '.join((
    "tcp.flags.syn == 1",
    "tcp.flags.push == 1",
    "tcp.flags.fin == 1",
    "tcp.flags.ack == 1"
)) + "'"

paths = {
    'test-cases':      ['cases',   '/share/test-cases'],
    'configuration':   ['conf',    '/share/conf'],
    'local-measures':  [None,      '/measures'],
    'shared-measures': ['reports', '/share/measures'],
}

startup_delay = shutdown_delay = 2