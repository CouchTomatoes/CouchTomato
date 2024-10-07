from couchtomato import app
from couchtomato import get_engine, web, base
from couchtomato.api import api
from couchtomato.core.settings.model import *
from couchtomato.environment import Env
from couchtomato.core.logger import CPLog
from logging import handlers
from argparse import ArgumentParser
import logging
import os.path
import sys


def cmd_couchtomato(base_path, args):
    '''Commandline entry point.'''

    # Options
    parser = ArgumentParser('usage: %prog [options]')
    parser.add_argument('-s', '--datadir', dest = 'data_dir', default = os.path.join(base_path, '_data'), help = 'Absolute or ~/ path, where settings/logs/database data is saved (default ./)')
    parser.add_argument('-t', '--test', '--debug', action = 'store_true', dest = 'debug', help = 'Debug mode')
    parser.add_argument('-q', '--quiet', action = 'store_true', dest = 'quiet', help = "Don't log to console")
    parser.add_argument('-d', '--daemon', action = 'store_true', dest = 'daemonize', help = 'Daemonize the app')

    options = parser.parse_args(args)

    # Create data dir if needed
    if not os.path.isdir(options.data_dir):
        options.data_dir = os.path.expanduser(options.data_dir)
        os.makedirs(options.data_dir)

    # Create logging dir
    log_dir = os.path.join(options.data_dir, 'logs');
    if not os.path.isdir(log_dir):
        os.mkdir(log_dir)

    # Daemonize app
    if options.daemonize:
        createDaemon()


    # Register environment settings
    Env.get('settings').setFile(os.path.join(options.data_dir, 'settings.conf'))
    Env.set('app_dir', base_path)
    Env.set('data_dir', options.data_dir)
    Env.set('db_path', os.path.join(options.data_dir, 'couchtomato.db'))

    # Determine debug
    debug = options.debug or Env.get('settings').get('debug', default = False)
    Env.set('debug', debug)


    # Logger
    logger = logging.getLogger()
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s', '%H:%M:%S')
    level = logging.DEBUG if debug else logging.INFO
    logger.setLevel(level)

    # To screen
    if debug and not options.quiet:
        hdlr = logging.StreamHandler(sys.stderr)
        hdlr.setFormatter(formatter)
        logger.addHandler(hdlr)

    # To file
    hdlr2 = handlers.RotatingFileHandler(os.path.join(log_dir, 'Couchtomato.log'), 'a', 5000000, 4)
    hdlr2.setFormatter(formatter)
    logger.addHandler(hdlr2)

    # Disable server access log as per debug value in setting config
    server_log = logging.getLogger('werkzeug')
    server_log.disabled = not debug

    # Start logging
    log = CPLog(__name__)
    log.debug('Started with params %s' % args)


    # Load configs
    from couchtomato.core.settings.loader import settings_loader
    settings_loader.load(root = base_path)
    settings_loader.addConfig('couchtomato', 'core')
    settings_loader.run()

    # Configure Database
    # from elixir import setup_all, create_all
    # setup_all()
    # create_all(get_engine())
    # https://stackoverflow.com/questions/16284537/creating-sqlite-database-if-it-doesnt-exist
    base.metadata.create_all(get_engine())


    # Create app
    api_key = Env.get('settings').get('api_key')
    url_base = '/' + Env.get('settings').get('url_base') if Env.get('settings').get('url_base') else ''
    reloader = debug and not options.daemonize

    # Basic config
    app.host = Env.get('settings').get('host', default = '0.0.0.0')
    app.port = Env.get('settings').get('port', default = 5000)
    app.debug = debug
    app.secret_key = api_key
    app.static_path = url_base + '/static'

    # Add static url with url_base
    # app.add_url_rule(app.static_path + '/<path:filename>',
    #                  endpoint = 'static',
    #                  view_func = app.send_static_file)

    # Register modules
    app.register_blueprint(web, url_prefix = '%s/' % url_base)
    app.register_blueprint(api, url_prefix = '%s/%s/%s/' % (url_base, 'api', api_key if not debug else 'apikey'))

    # Go go go!
    app.run(use_reloader = reloader)