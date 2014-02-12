"""
   users.py - 

   NOTE: this module should not be run as a standalone scripts, excepts for
   built-in tests.

"""
# HISTORY ####################################################################
#                       
# 0.0.1   Mar11   MR # This is just an example hot to write history notes
# 2       Dec12   MR # Added the implementation of the Password class
# 2.1     Dec12   MR # The Password class has been moved to its own module
# 3       Feb14   MR # Added a 'hint' property, to store password hint
#                       
##############################################################################
from __future__ import print_function
__description__ = "Users class implementation"
__version__ = "2"
_author__ = "Miran R."

import json
from enum import enum
from password import Password

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
        self._hint = hint
    
    def __str__(self):
        return "{}:{}:{}:{}:{}:{}".format(self.username, str(self.password), 
                self.role, self.fullname, self.email, self._hint)

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

    @property
    def hint(self):
        return self._hint

    def changePassword(self, old, new, confirmed):
        """Change password. If all strings (old password, new passsword
        and confirmed new password) are OK, change the user's password. 
        Returns the status: True if password changed, False if not."""
        status = False
        # only if old password has been matched, we create a new password   
        if self._pwd.compare(old):
            newpwd = Password(new)
            # if 'new' and 'confirmed' passwords are identical, we can change 
            # the password
            if newpwd.compare(confirmed):
                self._pwd = newpwd
                status = True
        return status

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
            d["hint"] = obj.hint
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
        if "hint" in d:
            hint = d["hint"]
        assert user is not None, "We need a username..."
        assert passwd is not None, "We need a password..." 
        return User(user, passwd, full, email, atype, hint)


# TESTING ####################################################################
def runtests():
    print("Starting tests....")
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
    print("\nChange password:")
    print(" case #1: new passwords do not match")
    status = u2.changePassword("blahblah", "newpassword", "NEWpassword");
    print("status = " + str(status))
    print(str(u2))
    print(" case #2: old password does not match")
    status = u2.changePassword("blablah", "newpassword", "newpassword");
    print("status = " + str(status))
    print(str(u2))
    print(" case #3: OK") 
    status = u2.changePassword("blahblah", "newpassword", "newpassword");
    print("status = " + str(status))
    print(str(u2))
    print("Stop.")

if __name__ == "__main__":
    print(__doc__)
    runtests()
