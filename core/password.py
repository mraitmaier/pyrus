"""
   users.py - 

   NOTE: this module should not be run as a standalone scripts, excepts for
   built-in tests.

"""
# HISTORY ####################################################################
#                       
# 1  Dec12  MR  Added the implementation of the Password class
# 2  Dec14  MR  Ported to Py3 (finally!)                     
##############################################################################

__description__ = "Password class implementation"
__version__ = "2"
_author__ = "Miran R."

import hashlib

# default password salt; salt can be configured
_PWD_SALT = "M1#'?_Xwqwqwe!!"

class Password(object):
    """ 
    Password - class representing a password

    This class hides the regular password behind the class instance.
    The class uses MD5 hashing algorithm and inserts the password salt before
    actual hashing. The default salt string is "weird" enough to be used, but
    nevertheless the custom salt string can be specified to a class
    constructor. 
    """

    def __init__(self, pwd, salt=_PWD_SALT):
        self._salt = salt
        self._pwd = self.__hash(pwd)

    def __str__ (self):
        return self._pwd

    def __hash(self, to_hash):    
        """Hashes (with MD5) the given password. Salt is also inserted into
        password before the actual hashing."""
        assert to_hash is not None
        return hashlib.md5(bytes(self._salt + to_hash, 'utf-8')).hexdigest()

    def compare(self, to_compare):
        """Compares the existing password with given string."""
        assert to_compare is not None
        status = False
        pwd_to_cmp = self.__hash(to_compare)
        if pwd_to_cmp == self._pwd:
            status = True
        return status


# TESTING ####################################################################
def runtests():
    print("Starting tests....")
    p = Password("blahblah")
    print(p)
    status = p.compare("nekajpaerwrwe")
    print("nekajpaerwrwe: "+ str(status))
    status = p.compare("blahblah")
    print ("blahblah: " + str(status))
    status = p.compare("blahBlah")
    print ("blahBlah: " + str(status))
    print("Stop.")

if __name__ == "__main__":
    print(__doc__)
    runtests()
