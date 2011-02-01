"""
Collection of utilities to help with the development of the PAS project.
"""


import os

from fabric.api import local, env, cd
from fabric.context_managers import show, settings


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


def _get_files():
    import pas
    ignored = set(('.DS_Store', 'pytidy.py', 'parser'))
    files = os.listdir(os.path.dirname(pas.__file__))
    files = (f for f in files if not f.endswith(".pyc"))
    files = (f for f in files if f not in ignored)
    files = (f.replace('.py', '') for f in files)
    files = ("pas." + f for f in files)
    files = ' '.join(files)
    
    return files

def pylint(modules=None, html=False):
    """
    Does a syntax and code-style check on the python code of this project
    using pylint.
    """
    modules = modules or _get_files()
    
    if html:
        local('mkdir -p temp')
        format = 'html >temp/pylint.html'
    else:
        format = 'text'
    
    with settings(show('everything'), warn_only=True):
        local("pylint --rcfile=pylint.ini {} --output-format={}".format(
              modules, format), capture=False)
        if html:
            local('open temp/pylint.html')