"""
Collection of utilities to help with the development of the PAS project.
"""


import os

from fabric.api import local, env, cd


def rcd(path):
    """
    relative-cd. Changes to the specified path under the basepath given by this
    fabfile filename.
    """
    return cd(os.path.join(os.path.dirname(__file__), path))


def sass():
    """
    Compiles the sass sources to css files.
    """
    with rcd("pas/conf/htdocs/sass"):
        local("compass compile", capture=False)

