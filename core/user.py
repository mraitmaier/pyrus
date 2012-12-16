"""
   users.py - 

   NOTE: this module should not be run as a standalone scripts, excepts for
   built-in tests.

"""
# HISTORY ####################################################################
#                       
# 0.0.1     Mar11   MR # This is just an example hot to write history notes
# 2         Dec12   MR # Added the implementation of the Password class
#                       
##############################################################################
from __future__ import print_function
__description__ = "Users class implementation"
__version__ = "2"
_author__ = "Miran R."

import json
from enum import enum
import hashlib

# default password salt; salt can be configured
PWD_SALT = "M1#'?_Xwqwqwe!!"

class Password(object):
    """ 
    Password - class representing a password

    This class hides the regular password behind the class instance.
    The class uses MD5 hashing algorithm and inserts the password salt before
    actual hashing. The default salt string is "weird" enough to be used, but
    nevertheless the custom salt string can be specified to a class
    constructor. 
    """

    def __init__(self, pwd, salt=PWD_SALT):
        self._salt = salt
        self._pwd = self.__hash(pwd)

    def __str__ (self):
        return self._pwd

    def __hash(self, to_hash):    
        """Hashes (with MD5) the given password. Salt is also inserted into
        password before the actual hashing."""
        assert to_hash is not None
        return hashlib.md5(self._salt + to_hash).hexdigest()

    def compare(self, to_compare):
        """Compares the existing password with given string."""
        assert to_compare is not None
        status = False
        pwd_to_cmp = self.__hash(to_compare)
        if pwd_to_cmp == self._pwd:
            status = True
        return status


# Role is an enum
Role = enum(("GUEST", "USER", "TESTER", "DEVELOPER", "MANAGER", "ADMIN",
             "UNKNOWN"))
def toRole(strVal):
    """ """
    strVal = strVal.lower().strip()
    val = Role.GUEST
    if strVal in ["user"]:
        val = Role.USER
    elif strVal in ["admin", "administrator", "administrators"]:
        val = Role.ADMIN
    elif strVal in ["test", "tester"]:
        val = Role.TESTER
    elif strVal in ["dev", "develop", "developer"]:
        val = Role.DEVELOPER
    elif strVal in ["mgr", "manager"]:
        val = Role.MANAGER
    elif strVal == "guest":
        val = Role.GUEST
    else:
        val = Role.UNKNOWN
    return val


class User(object):
    """
        User - class used for username/password administration 
    """

    def __init__(self, username, password, 
                       fullname="", email="", role=Role.TESTER, hint=""):
        assert username is not None
        assert password is not None
        self._user = username
        self._pwd = Password(password)
        self._name = fullname
        self._type = role
        self._email = email
    
    def __str__(self):
        #return "{:>24}: {:>16}/{:>16} ({:32}) {:8}".format(self.fullname, 
        return "{}: {}/{} ({}) {}".format(self.fullname, self.username, 
                          str(self.password), self.email, self.role)

    @property
    def username(self):
        return self._user

    @property
    def password(self):
        return str(self._pwd)

    @property
    def fullname(self):
        return self._name

    @property
    def role(self):
        return self._type

    @property
    def email(self):
        return self._email

    def changePassword(self, old, new, confirmed):
        # only if old password has been matched, we create a new password   
        if self.password.compare(old):
            newpwd = Password(new)
            # if 'new' and 'confirmed' passwords are identical, we can change 
            # the password
            if newpwd.compare(confirmed):
                self._pwd = newpwd

    def toJson(self):
        return json.dumps(self, indent=4, cls=_UserJsonEncoder)

class _UserJsonEncoder(json.JSONEncoder):
    """Custom JSON encoder for User class"""
    
    def default(self, obj):
        if isinstance(obj, User):
            d = dict()
            d["username"] = obj.username
            d["password"] = obj.password
            d["fullname"] = obj.fullname
            d["role"]  = obj.role
            d["email"] = obj.email
            return d
        return json.JSONEncoder(obj)

class UserJsonDecoder(json.JSONDecoder):
    """Custom JSON decoder for User class"""
    
    def decode(self, jsontext):
        d = json.loads(jsontext)
        #
        user = None
        passwd = None
        full = ""
        atype = Role.GUEST
        #
        if "username" in d:
            user = d["username"]
        if "password" in d:
            passwd = d["password"]
        if "fullname" in d:
            full = d["fullname"]
        if "role" in d:
            atype = toRole(d["role"])
        if "email" in d:
            email = d["email"]
        assert user is not None, "We need a username..."
        assert passwd is not None, "We need a password..." 
        return User(user, passwd, full, email, atype)


# TESTING ####################################################################
def test_password():
    p = Password("blahblah")
    print(p)
    status = p.compare("nekajpaerwrwe")
    print("nekajpaerwrwe: "+ str(status))
    status = p.compare("blahblah")
    print ("blahblah: " + str(status))
    status = p.compare("blahBlah")
    print ("blahBlah: " + str(status))


def runtests():
    print("Starting tests....")
    test_password()
    print("")
    u = User("miran", "blahblah", "Miran Raitmaier", "mraitmaier@aviatnet.com",
            Role.ADMIN)
    print(str(u))
    j = u.toJson()
    print(j)
    u1 = UserJsonDecoder().decode(j)
    print(str(u1))
    u2 = User("mirko", "blahblah", "Miroslav Novak", "mnovak@eion.com",
            Role.MANAGER)
    print(str(u2))
    j = u2.toJson()
    print(j)
    u3 = UserJsonDecoder().decode(j)
    print(str(u3))
    print("Stop.")

if __name__ == "__main__":
    print(__doc__)
    runtests()
