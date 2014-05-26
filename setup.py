import sys

from setuptools import setup, find_packages


setup(
    name='conway',
    version='1.1',
    description="A simple, colorful Game Of Life demo on the terminal",
    long_description=open('README.rst').read(),
    author='Erik Rose',
    author_email='erikrose@grinchcentral.com',
    license='MIT',
    packages=find_packages(exclude=['ez_setup']),
    scripts=['bin/conway.py'],
    url='https://github.com/erikrose/conway',
    include_package_data=True,
    install_requires=['blessings>=1.5,<2.0'],
    classifiers=[
        'Environment :: Console',
        'Environment :: Console :: Curses',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Artistic Software',
        'Topic :: Games/Entertainment :: Simulation',
        'Topic :: Scientific/Engineering :: Artificial Life',
        'Topic :: Terminals'
        ],
    keywords=['terminal', 'tty', 'console', 'game', 'life']
)
