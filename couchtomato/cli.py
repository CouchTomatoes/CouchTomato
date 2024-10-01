from blinker import signal
from couchtomato import app
from couchtomato.settings import Settings
from logging import handlers
from optparse import OptionParser
import logging
import os.path
import sys

def cmd_couchtomato(base_path):
    '''Commandline entry point.'''
    
    # Options
    parser = OptionParser('usage: %prog [options]')
    parser.add_option('-l', '--logdir', dest = 'logdir', default = 'logs', help = 'log DIRECTORY (default ./logs)')
    parser.add_option('-t', '--test', '--debug', action = 'store_true', dest = 'debug', help = 'Debug mode')
    parser.add_option('-q', '--quiet', action = 'store_true', dest = 'quiet', help = "Don't log to console")
    parser.add_option('-d', '--daemon', action = 'store_true', dest = 'daemon', help = 'Daemonize the app')
    (options, args) = parser.parse_args(sys.argv[1:])
    # Register settings
    settings = Settings('settings.conf')
    register = signal('settings_register')
    register.connect(settings.registerDefaults)
    debug = "False" #options.debug or settings.get('environment') == 'development'
    # Logger
    logger = logging.getLogger()
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s', '%H:%M:%S')
    level = logging.DEBUG if debug else logging.INFO
    logger.setLevel(level)
    # Output logging information to screen
    if not options.quiet:
        hdlr = logging.StreamHandler(sys.stderr)
        hdlr.setFormatter(formatter)
        logger.addHandler(hdlr)
    # Output logging information to file
    hdlr2 = handlers.RotatingFileHandler(os.path.join(options.logdir, 'Couchtomato.log'), 'a', 5000000, 4)
    hdlr2.setFormatter(formatter)
    logger.addHandler(hdlr2)
    # Load config
    from couchtomato.settings.loader import SettingsLoader
    SettingsLoader(root = base_path)
    # Create app
    # ToDO The config are not getting fetched at all on line 24, and 44 and on 36 directory has to be created if not exists which was not working until I created the log folder
    # app.run(host = settings.get('host'), port = int(settings.get('port')), debug = debug)
    app.run(host = '0.0.0.0', port = '5050', debug = debug)