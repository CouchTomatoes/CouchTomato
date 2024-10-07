#!/usr/bin/env python
"""You need to have setuptools installed. Use command
pip install setuptools

Usage:
    python setup.py develop

This will register the couchtomato package in your system and thereby make it
available from anywhere.

Also, a script will be installed to control couchtomato from the shell.
Try running:
    couchtomato --help

"""
from setuptools import setup

setup(name="couchtomato",
      packages=['couchtomato'],
      install_requires=[
          'argparse',
          'flask',
          'nose',
          'sqlalchemy'],
      entry_points="""
      [console_scripts]
      couchtomato = couchtomato.cli:cmd_couchtomato
      """)