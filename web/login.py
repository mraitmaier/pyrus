##############################################################################
# login.py - 
##############################################################################
from pyrus.web.bottle import  get, post, template, request
from pyrus.core.user import User

_USER_CFG_FILE = '../cfg/users.cfg'

@get('/')
@get('/login')
@get('/login/')
def login_get():
    return template('login')

@post('/')
@post('/login')
@post('/login/')
def login_post():
    name = request.forms.get('username')
    pwd = request.forms.get('password')
    if check_user(name, pwd):
        return template('index')
    return template('login')

def check_user(user, pwd):
    '''
    check_user - a function that validates the username and pasword
    '''
    u = User(name, pwd)

    return True
