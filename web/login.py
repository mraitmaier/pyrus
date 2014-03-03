##############################################################################
# login.py - 
##############################################################################
#from bottle import  get, post, template, request
import bottle
from pyrus.core.user.user import User
from main import post_get, postd, aaa

#_USER_CFG_FILE = '../cfg/users.cfg'

#@bottle.get('/')
@bottle.get('/login')
@bottle.get('/login/')
def login_get():
    return template('login')

#@bottle.post('/')
@bottle.post('/login')
@bottle.post('/login/')
def login_post():
    name = post_get('username')
    pwd = post_get('password')
    aaa.login(name, pwd, success_redirect='/index', fail_redirect='/login')
##    if check_user(name, pwd):
##        return template('index')
##    return template('login')

def check_user(user, pwd):
    '''
    check_user - a function that validates the username and pasword
    '''
    u = User(name, pwd)

    return True
