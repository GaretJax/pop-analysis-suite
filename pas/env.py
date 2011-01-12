"""
General test suite environment management functions.
"""


import os
import shutil

import pas.conf


def setup(dstdir):
    """
    Sets up a new environment in the given directory by recursively copying
    all the files inside pas.conf.suite_template to the given directory.
    
    The destination directory must already exist.
    """
    srcdir = os.path.join(os.path.dirname(pas.conf.__file__), 'suite_template')
    
    # Copy each child individually to the exising directory. shutil.copytree
    # cannot be used directly because the target directory already exists.
    for i in os.listdir(srcdir):
        src = os.path.join(srcdir, i)
        dst = os.path.join(dstdir, i)
        
        if os.path.isdir(src):
            shutil.copytree(src, dst)
        else:
            shutil.copy(src, dst)

