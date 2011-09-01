"""
   PythonScript.py - python script implementing the PythonScript class

   This class is used to run python scripts from python.

   NOTE: This script is not to be run standalone (except for the testing
         purposes), it is meant to be used a module.
"""
# HISTORY ####################################################################
#
##############################################################################
__description__ = "a PythonScript class implementation"
__version__ = "0.0.1"
__author__ = "Miran R."

import os
from executable import Executable
#from subprocess import Popen, PIPE, STDOUT

_EXECUTABLE = "python"

class PythonScript(Executable):
    """
        PythonScript - executable wrapper for python script
    """

    def __init__(self, script):
        super(PythonScript, self).__init__(script)

    def execute(self, args=""):
        """Executes the Python script"""
        return super(PythonScript, self).execute(_EXECUTABLE, args)

# TESTING ###################################################################
TEST_SCRIPT = "test/scripts/test.py"   # existing script
NO_SCRIPT = "test/scripts/tst.py"      # non-existing script

def runtests():
    sc = PythonScript(TEST_SCRIPT)
    print(sc.environ)
    print("Executing '{}'...".format(sc.command))
    print(str(sc))
    rc, output = sc.execute()
    print("OUTPUT:\n'{}'".format(output))
    print("RC={}".format(rc))
    print("########## args test")
    sc = PythonScript(TEST_SCRIPT)
    print("Executing '{}'...".format(sc.command))
    print(str(sc))
    rc, output = sc.execute("arg1 arg2 arg3")
    print("OUTPUT:\n'{}'".format(output))
    print("RC={}".format(rc))
    print("########## real args test")
    sc = PythonScript(TEST_SCRIPT)
    print(sc.command)
    print("Executing...")
    rc, output = sc.execute()
    print(str(sc))
    print("OUTPUT:\n'{}'".format(output))
    print("RC={}".format(rc))
    print("########## non-existing script")
    sc = PythonScript(NO_SCRIPT)
    print("Executing '{}'...".format(sc.command))
    rc, output = sc.execute()
    print(str(sc))
    print("OUTPUT:\n'{}'".format(output))
    print("RC={}".format(rc))


if __name__ == "__main__":
    print __doc__
    runtests()

