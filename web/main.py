#!/usr/bin/env python
##############################################################################
# main.py - 
##############################################################################
_VERSION="1"
_AUTHOR="Miran R."
_NAME="Pyrus main web module"

from pyrus.web.bottle import get, run, static_file

# page definitions
from license import license
from login import login, login_submit

# we serve static JavaScript files...
@get('/<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root='static/js')

# ... and CCS files...
@get('/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='static/css')

# ... and images...
@get('/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root='static/img')

# ... and fonts...
@get('<filename:re:.*\.(ttf|otf|svg|woff)>')
def fonts(filename):
    return static_file(filename, root='static/fonts')

# ... and finally static HTML pages.
@get('<filename:re:.*\.(htm|html)>')
def static_html_pages(filename):
    return static_file(filename, root='static/html')

run(host='localhost', port=8080, debug=True)
