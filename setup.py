#!/usr/bin/env python3
from setuptools import setup

setup(
    name='turtetris',
    version='0.1',
    description="Turris Tetris",
    long_description="Tetris game played on ten Turris Omnias stacked on top of each other.",
    url="https://github.com/Cynerd/mcserver-wrapper",
    author="Cynerd",
    author_email="cynerd@email.cz",
    license="GPLv2",

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        ],
    keywords='Turris Tetris',

    packages=['turtetris'],
    entry_points={
        'console_scripts': [
            'turtetris-master=turtetris-master'
            ]
        }
    )
