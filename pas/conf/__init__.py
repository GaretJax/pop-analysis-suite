"""
Settings support for the whole pas package.

This module contains methods to load and temporarily store setting directives
for the current execution.

Various shortcuts to access the different settings in a usage-oriented way are
also provided.
"""


from collections import defaultdict
import itertools
import logging
import os
import sys


__all__ = ['settings', 'all_hosts', 'role', 'map_interfaces']


class Settings(object):
    """
    A simple settings store which is able to load variables defined in a
    module.
    """
    
    def __init__(self, defaults=None):
        """
        Creates a new Setting instance by loading the optional defaults from
        the given module.
        """
        self.last_path = None
        
        if defaults:
            if isinstance(defaults, basestring):
                self.loadfrompath(module=defaults)
            else:
                self.load(defaults)
    
    def load(self, module):
        """
        Loads the given module by copying all its public defined variables
        to the instance.
        
        Older keys are overridden by new ones.
        """
        log = logging.getLogger()
        log.debug("Loading settings from '{0}'".format(module.__file__))
        
        for key, value in module.__dict__.iteritems():
            if not key.startswith('_') and key.isupper():
                setattr(self, key, value)
    
    def loadfrompath(self, path=None, module='settings'):
        """
        Loads the setting directives from the given module, by looking first
        in the provided path.
        """
        log = logging.getLogger()
        
        if path:
            sys.path.insert(0, path)
        
        try:
            __import__(module, level=0)
            _settings = sys.modules[module]
        except ImportError:
            log.debug("Could not load settings, module not found on path:")
            
            for i in sys.path:
                log.debug(" - checked: {0}".format(i))
            
            raise
        else:
            self.ENV_BASE = os.path.dirname(_settings.__file__)
            self.load(_settings)
        finally:
            if path:
                sys.path.pop(0)
    
    def get(self, name, default=None):
        """
        Gets a setting directive falling back to the provided default, thus
        not generating any errors.
        """
        return getattr(self, name, default)
    
    def __str__(self):
        """
        Returns a string representation of this settings object, containing
        the a key=value pair on each line.
        """
        directives = []
        
        for key, value in self.__dict__.iteritems():
            directives.append('{0}={1}'.format(key, value))
        
        return '\n'.join(directives)
    
    def __getattr__(self, name):
        """
        Raises a custom exception if the attribute was not found.
        """
        raise AttributeError("The requested setting directive ({0}) is " \
                             "not set".format(name))


# pylint: disable-msg=C0103
# Uff... module level variables should all be uppercase, but this is a special
# case (hope Guido is not going to read this).

settings = Settings('pas.conf.basesettings')

# pylint: enable-msg=C0103


def stylesheet(name):
    """
    Returns the full path to the XSL stylesheet with the given name inside the
    directory defined in the confguration path.
    """
    return os.path.join(settings.PATHS['configuration'][0], 'templates', name)


def all_hosts():
    """
    Returns a set of all hosts obtained by chaining all hosts in the ROLES
    settings directive.
    """
    return set(itertools.chain(*settings.ROLES.values()))


def role(role_name):
    """
    Returns a list of all hosts for a given role.
    """
    return settings.ROLES[role_name]


def map_interfaces():
    """
    Returns a dict mapping host connection strings to interfaces, obtained by
    combining the INTERFACES and ROLES settings directives.
    """
    mapping = defaultdict(set)

    for role_name, hosts in settings.ROLES.iteritems():
        for host in hosts:
            try:
                mapping[host] |= set(settings.INTERFACES[role_name])
            except KeyError:
                pass

    return mapping.iteritems()

