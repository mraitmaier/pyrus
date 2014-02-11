##############################################################################
# license.py - 
##############################################################################
from pyrus.web.bottle import  get, post, template, request
from pyrus.core.user import User

@get('/license')
@get('/license/')
def license():
    return template('license')

