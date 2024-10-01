#!/usr/bin/env python
"""Wrapper for the command line interface."""

from os.path import dirname, isfile
import os
import subprocess
import sys
import traceback

# Root path
base_path = dirname(os.path.abspath(__file__))
# Insert local directories into path
sys.path.insert(0, os.path.join(base_path, 'libs'))

from couchpotato.core.logger import CPLog
log = CPLog(__name__);

try:
    from couchtomato import cli
except ImportError:
    print ("Checking local dependencies...")
    if isfile(__file__):
        cwd = dirname(__file__)
        print ("Updating libraries...")
        stdout, stderr = subprocess.Popen(["git", "submodule", "init"],
                                          stderr = subprocess.PIPE,
                                          stdout = subprocess.PIPE).communicate()
        if stderr:
            print ("[WARNING] Git is complaining:")
            print ("=" * 78)
            print (stderr)
            print ("=" * 78)
        stdout, stderr = subprocess.Popen(["git", "submodule", "update"],
                                          stderr = subprocess.PIPE,
                                          stdout = subprocess.PIPE).communicate()
        if stderr:
            print ("[WARNING] Git is complaining:")
            print ("=" * 78)
            print (stderr)
            print ("=" * 78)
        #print ("Registering libraries...")
        # Insert local directories into path
        #lib_path = os.path.join(os.path.abspath(cwd), 'libs')
        #src_path = os.path.join(os.path.abspath(cwd), 'src')
        #sys.path.insert(0, lib_path)
        #sys.path.insert(0, src_path)
        print (sys.path)
        print ("Passing execution to couchtomato...")
        try:
            from couchtomato import cli
        except ImportError:
            print ("[ERROR]: Something's seriously wrong.")
            print ("=" * 78)
            traceback.print_exc()
            print ("=" * 78)
            print ("Aborting...")
            sys.exit(1)
    else:
        # Running from Titanium
        raise NotImplementedError("Don't know how to do that.")

if __name__ == "__main__":
    try:
        cli.cmd_couchpotato(base_path)
    except Exception as e:
        log.critical(e)