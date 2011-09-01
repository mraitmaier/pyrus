"""
   users.py - 

   NOTE: this module should not be run as a standalone scripts, excepts for
   built-in tests.

"""
# HISTORY ####################################################################
#                       
# 0.0.1     Mar11   MR # This is just an example hot to write history notes
#                       
##############################################################################
__description__ = "Users class implementation"
__version__ = "0.1"
_author__ = "Miran R."

import json

def toRoleValue(strVal):
    """ """
    strVal = strVal.lower().strip()
    val = Role.GUEST
    if strVal in ["user"]:
        val = Role.USER
    elif strVal in ["admin", "administrator", "administrators"]:
        val = Role.ADMIN
    return val

def roleToString(val):
    """ """
    if val == Role.USER:
        return "user"
    elif val == Role.ADMIN:
        return "administrator"
    elif val == Role.GUEST:
        return "guest"
    else:
        raise ValueError("Invalid user role value")

class Role(object):
    """
        Role - class representing the possible user roles
    """
    USER = 0
    GUEST = 1
    ADMIN = 2
    values = [USER, GUEST, ADMIN]
    
    @staticmethod
    def convert(strVal):
        """Converts a string value into integer"""
        strVal = strVal.lower().strip()
        val = Role.GUEST
        if strVal in ["user"]:
            val = Role.USER
        elif strVal in ["admin", "administrator", "administrators"]:
            val = Role.ADMIN
        return val

    @staticmethod
    def toString(val):
        """ """
        if val == Role.USER:
            return "user"
        elif val == Role.ADMIN:
            return "admin"
        elif val == Role.GUEST:
            return "guest"
        else:
            return "unknown role"

class User(Exception):
    """
        User - class used for username/password administration 
    """

    def __init__(self, username, password, 
                       fullname="", email="", role=Role.USER):
        assert username is not None
        assert password is not None
        assert role in Role.values
        self._user = username
        self._pwd = password
        self._name = fullname
        self._type = role
        self._email = email
    
    def __str__(self):
        #return "{:>24}: {:>16}/{:>16} ({:32}) {:8}".format(self.fullname, 
        return "{}: {}/{} ({}) {}".format(self.fullname, self.username, 
                          self.password, self.email, Role.toString(self.role))

    @property
    def username(self):
        return self._user

    @property
    def password(self):
        return self._pwd

    @property
    def fullname(self):
        return self._name

    @property
    def role(self):
        return self._type

    @property
    def email(self):
        return self._email

    def changePassword(old, new, confirmed):
        if old == self._pwd and new == confirmed:
            self._pwd = new

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
            d["role"]  = Role.toString(obj.role)
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
            atype = Role.convert(d["role"])
        if "email" in d:
            email = d["email"]
        assert user is not None, "We need a username..."
        assert passwd is not None, "We need a password..." 
        return User(user, passwd, full, email, atype)

# TESTING ####################################################################
def runtests():
    print("Starting tests....")
    u = User("miran", "blahblah", "Miran Raitmaier", "mraitmaier@aviatnet.com",
            Role.ADMIN)
    print(str(u))
    j = u.toJson()
    print(j)
    u1 = UserJsonDecoder().decode(j)
    print(str(u1))
    print("Stop.")

if __name__ == "__main__":
    print(__doc__)
    runtests()
