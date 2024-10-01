#!/usr/bin/env python
"""Wrapper for the command line interface."""

import os
from os.path import dirname, isfile
import subprocess
import sys


try:
    from couchtomato import cli
except ImportError:
    print ("Checking local dependencies...")
    if isfile(__file__):
        cwd = dirname(__file__)
        print ("Updating libraries...")
        stdout, stderr = subprocess.Popen(["git", "submodule", "init"],
                                          stderr=subprocess.PIPE,
                                          stdout=subprocess.PIPE).communicate()
        if stderr:
            print ("[WARNING] Git is complaining:")
            print ("="*78)
            print (stderr)
            print ("="*78)
        stdout, stderr = subprocess.Popen(["git", "submodule", "update"],
                                          stderr=subprocess.PIPE,
                                          stdout=subprocess.PIPE).communicate()
        if stderr:
            print ("[WARNING] Git is complaining:")
            print ("="*78)
            print (stderr)
            print ("="*78)
        print ("Registering libraries...")
        # Insert local directories into path
        lib_path = os.path.join(os.path.abspath(cwd), 'libs')
        src_path = os.path.join(os.path.abspath(cwd), '/')
        sys.path.insert(0, lib_path)
        sys.path.insert(0, src_path)
        print ("Passing execution to couchtomato...")
        try:
            from couchtomato import cli
        except ImportError:
            print ("[ERROR]: Something's seriously wrong.")
            print ("Could not load couchtomato from directory.")
    else:
        # Running from Titanium
        raise NotImplementedError("Don't know how to do that.")


cli.cmd_couchtomato()