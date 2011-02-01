
import os, itertools
from setuptools import setup, find_packages
 
version = '0.1'

def read(fname):
    """
    Utility function to read the README file.
    """
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def get_files(base):
    """
    Utility function to list all files in a data directory.
    """
    base = os.path.join(os.path.dirname(__file__), *base.split('.'))
    
    rem = len(os.path.dirname(base)) + 1
    
    for root, dirs, files in os.walk(base):
        for name in files:
            yield os.path.join(root, name)[rem:]

setup(
    name='pas',
    version=version,
    description="POP Analysis Suite",
    long_description=read('README.md'),
    classifiers=[
        'Development Status :: 4 - Beta',
    ],
    keywords='',
    author='Jonathan Stoppani',
    author_email='jonathan.stoppani@edu.hefr.ch',
    url='https://github.com/GaretJax/pop-analysis-suite',
    license='MIT',
    packages=find_packages(exclude=['tests']),
    install_package_data=True,
    package_data = {
        'pas.conf': 
            list(get_files('pas.conf.suite_template')) +
            list(get_files('pas.conf.htdocs'))) +
            list(get_files('pas.conf.templates')))
    },
    install_requires=[
        'fabric',
        'lxml',
        'pygments',
        'argparse',
    ],
    entry_points=read('entry_points.ini')
)
