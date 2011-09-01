"""
   testobject.py - 

   NOTE: this module should not be run as a standalone scripts, excepts for
   built-in tests.

"""
# HISTORY ####################################################################
#                       
# 0.0.1     Mar11   MR # This is just an example hot to write history notes
#                       
##############################################################################
__description__ = "a TestObject class implementation"
__version__ = "0.0.1"
_author__ = "Miran R."

class TestObjectType(object):
    UNKNOWN = -1
    HARDWARE = 0
    SOFTWARE = 1
    valid = [UNKNOWN, HARDWARE, SOFTWARE]

class TestObject(object):
    """
        TestObject -
    """

    def __init__(self, name, otype=TestObjectType.UNKNOWN, version=None,
                             ip="0.0.0.0", description=""):
        self._name = name
        self._type = otype
        self._version = version
        self._description = description
        self._ip = ip

    def __str__(self):
        s = "\n".join(("TestObject: {}".format(self.name),
                       "  type: {}".format(self.objtypeString()),
                       "  version: {}".format(self.version),
                       "  IP address: {}".format(self.ip),
                       "  description:\n{}".format(self.description)
                  ))
        return s

    @property    
    def name(self):
        return self._name

    @property
    def objtype(self):
        return self._type

    @property
    def version(self):
        return self._version

    @property
    def ip(self):
        return self._ip

    @property
    def description(self):
        return self._description

    def objtypeString(self):
        if self.objtype == TestObjectType.UNKNOWN:
            return "unknown"
        elif self.objtype == TestObjectType.HARDWARE:
            return "hardware"
        elif self.objtype == TestObjectType.SOFTWARE:
            return "software"
        else:
            return "test object value error"

 # TESTING ####################################################################
def runtests():
    print("Starting unit tests...")
    to = TestObject("a test object")
    print(str(to))
    print("Stop")

if __name__ == '__main__':
   print(__doc__)
   runtests()
