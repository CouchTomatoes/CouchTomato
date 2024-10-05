#!/usr/bin/env python
# -*- coding: utf-8 -*-
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

from couchtomato.core.logger import CPLog
log = CPLog(__name__)

try:
    from couchtomato import cli
except ImportError:
    log.info("Checking local dependencies...")
    if isfile(__file__):
        cwd = dirname(__file__)
        log.info("Updating libraries...")
        stdout, stderr = subprocess.Popen(['git', 'submodule', 'init'],
                                          stderr = subprocess.PIPE,
                                          stdout = subprocess.PIPE).communicate()
        if stderr:
            log.info("[WARNING] Git is complaining:")
            log.info(stderr)
        stdout, stderr = subprocess.Popen(['git', 'submodule', 'init'],
                                          stderr = subprocess.PIPE,
                                          stdout = subprocess.PIPE).communicate()
        if stderr:
            log.info("[WARNING] Git is complaining:")
            log.info(stderr)
        
        log.info("Passing execution to couchtomato...")
        try:
            from couchtomato import cli
        except ImportError:
            log.error("[ERROR]: Something's seriously wrong.")
            log.error(traceback.print_exc())
            sys.exit(1)
            
    else:
        # Running from Titanium
        raise NotImplementedError("Don't know how to do that.")

if __name__ == "__main__":
    try:
        cli.cmd_couchtomato(base_path, sys.argv[1:])
    except Exception as e:
        log.critical(e)