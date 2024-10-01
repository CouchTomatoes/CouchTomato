#!/usr/bin/env python

from setuptools import setup

setup(name="couchtomato",
      packages=['couchtomato'],
      package_dir={'': 'src'},
      install_requires=[
          'argparse',
          'sqlalchemy',
          'elixir',
          'nose'],
      entry_points="""
      [console_scripts]
      couchtomato = couchtomato.cli:cmd_couchtomato
      """)