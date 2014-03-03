#!/usr/bin/env python
##############################################################################
# main.py - 
##############################################################################
_VERSION="1"
_AUTHOR="Miran R."
_NAME="Pyrus main web module"

import sys
import os
from core.cfgfile import read_config_file 
import bottle
from pyrus.web.beaker.middleware import SessionMiddleware
import logging, logging.handlers

from key import _generate_key

# page definitions
#from license import license
#from login import login_get, login_post
#from index import index

# default path for storing session file
_DEFAULT_SESSION_PATH = './session'
# default path for log file
_DEFAULT_LOG_PATH = './log/pyrusweb.log'

# global var that stores the app configuration params
#Cfg = None
# read configuration file and store the params
Cfg = read_config_file()

# turn on the bottle debugging
bottle.debug(True) # DEBUG

# session middleware stuff...
if 'session_file_path' in Cfg:
    sess_path = Cfg['session_file_path'] 
else:
    sess_path = _DEFAULT_SESSION_PATH
session_opts = {
        'session.data_dir': sess_path,
        'session.cookie_expires': True,
        'session.httponly': True,
        'session.timeout': 3600*8, # 8 hours
        'session.cookie_expires': True,
        'session.type': 'file',
        'session.encrypt_key': _generate_key() ,
        'session.validate_key': True,
        'session.auto': True
}
app = SessionMiddleware(bottle.app(), session_opts)
#session = bottle.request.environ.get('beaker.session')
#log.info('Session middleware configured.')
#log.info('Session file is located in "%s".' % sess_path)

# aux bottle funcs
def postd():
    return bottle.request.forms

def post_get(name, default=''):
    return bottle.request.POST.get(name, default).strip()

def authenticated(func):
    '''Decorator to check whether current user is logged in.
    source: http://stackoverflow.com/questions/11698473/
             bottle-hooks-with-beaker-session-middleware-and-checking-logins
    '''
    def wrapped(*args, **kwargs):

        try:
            sess = bottle.request.environ.get('beaker.session')
        except:
            return bottle.abort(401, 'Failed beaker_session in slash')

        try:
            name = sess['name']
            return func(*args, **kwargs)
        except:
            bottle.redirect('/login')
    return wrapped    

# we serve static JavaScript files...
@bottle.get('/<filename:re:.*\.js>')
def javascripts(filename):
    return bottle.static_file(filename, root='static/js')

# ... and CCS files...
@bottle.get('/<filename:re:.*\.css>')
def stylesheets(filename):
    return bottle.static_file(filename, root='static/css')

# ... and images...
@bottle.get('/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return bottle.static_file(filename, root='static/img')

# ... and fonts...
@bottle.get('<filename:re:.*\.(ttf|otf|svg|woff)>')
def fonts(filename):
    return bottle.static_file(filename, root='static/fonts')

# ... and finally static HTML pages.
@bottle.get('<filename:re:.*\.(htm|html)>')
def static_html_pages(filename):
    return bottle.static_file(filename, root='static/html')

@bottle.get('/login')
def login_get():
    return bottle.template('login')

@bottle.post('/login')
def login():
    '''Authenticate users'''
    username = post_get('username')
    password = post_get('password')
    sess = bottle.request.environ.get('beaker.session')
    sess['name'] = username
    return bottle.template('index', username=username)

@bottle.route('/logout')
@authenticated
def logout():
    sess = bottle.request.environ.get('beaker.session')
    del sess['name'] 
    bottle.redirect('/login')

@bottle.get('/license')
@authenticated
def license():
    sess = bottle.request.environ.get('beaker.session')
    return bottle.template('license', username=sess['name'])

@bottle.route('/')
@bottle.route('/index')
@authenticated
def index():
    ''' '''
    sess = bottle.request.environ.get('beaker.session')
    return bottle.template('index', username=sess['name'])

def user_is_logged(session, username):
    return username in session
    
def create_logger(filename, syslog=None, debug=False):
    '''Creates the logger and the appropriate handlers.'''
    log = logging.getLogger("PyrusWeb")
    log.setLevel(logging.INFO)
    timeForm = "%Y-%m-%d %H:%M:%S"
    f1 = logging.Formatter("%(asctime)s - %(name)s - %(message)s", timeForm)
    f2 = logging.Formatter(
              "%(asctime)s - %(name)s - %(levelname)s - %(message)s", timeForm)
    # default handler is sys.stdout
    sHandler = logging.StreamHandler(sys.stdout)
    sHandler.setLevel(logging.WARNING)
    sHandler.setFormatter(f1)
    log.addHandler(sHandler)
    # we specify logging to file
    fHandler = logging.FileHandler(filename, mode="w", encoding="utf-8")
    fHandler.setFormatter(f2)
    log.addHandler(fHandler)
    log.warning("Logger created successfully")
    log.warning("Everything will be logged to '{}'".format(filename))
    # syslog logger is added if syslog IP address is specified
    if syslog is not None and check_ip(syslog):
        nHandler = logging.handlers.SysLogHandler((syslog, 514))
        nHandler.setFormatter(f2)
        log.addHandler(nHandler)
        log.warning("Syslog logger created: '{}".format(syslog))
    else:
        log.warning( "Syslog logger will NOT be created.")
    if debug:
        log.setLevel(logging.DEBUG)
        log.warning("Debug mode enabled.")
    return log

if __name__ == "__main__":

    # create loggers
    logfile = Cfg['log_file'] if 'log_file' in Cfg else _DEFAULT_LOG_FILE
    log = create_logger(logfile, None)

    # run web app 
    bottle.run(app=app, host='localhost', port=8080, reloader=True)
