from setuptools import setup, find_packages
 
version = '0.1'
 
setup(name='pas',
    version=version,
    description="POP Analysis Suite",
    long_description="""A VM based communication analyzer for the POP (Parallel Object Programming) model.""",
    classifiers=[],
    keywords='',
    author='Jonathan Stoppani',
    author_email='jonathan.stoppani@edu.hefr.ch',
    url='',
    license='MIT',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    install_requires=[
        'fabric',
        'lxml',
        'pygments',
    ],
    entry_points="""
[console_scripts]
pas = pas.bin.pas:main
"""
)