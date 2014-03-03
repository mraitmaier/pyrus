##############################################################################
# license.py - 
##############################################################################
from bottle import  get, post, template, request
#from pyrus.core.user.user import User

@get('/license')
@get('/license/')
def license():
    return template('license')

