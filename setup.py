
import os
from setuptools import setup, find_packages
 
version = '0.1'

def read(fname):
    """
    Utility function to read the README file.
    """
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


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
    include_package_data=True,
    install_requires=[
        'fabric',
        'lxml',
        'pygments',
        'argparse',
    ],
    entry_points=read('entry_points.ini')
)
