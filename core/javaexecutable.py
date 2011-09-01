"""
   JavaExecutable.py - java script implementing the JavaExecutable class

   This class is used to run java executables from python.

   NOTE: This script is not to be run standalone (except for the testing
         purposes), it is meant to be used a module.
"""
# HISTORY ####################################################################
# 0.0.1     Mar11   MR  Initial version.
#
##############################################################################
__description__ = "a JavaExecutable class implementation"
__version__ = "0.0.1"
__author__ = "Miran R."

import os
from executable import Executable
#from subprocess import Popen, PIPE, STDOUT

_EXECUTABLE = ["java", "-jar"]

class JavaExecutable(Executable):
    """
        JavaExecutable - executable wrapper for java executable
    """

    def __init__(self, script):
        super(JavaExecutable, self).__init__(script)

    def execute(self, args=""):
        """Executes the Java executable"""
        return super(JavaExecutable, self).execute(_EXECUTABLE, args)

# TESTING ###################################################################
TEST_SCRIPT = "test/scripts/hello.jar"   # existing script
NO_SCRIPT = "test/scripts/blah.jar"      # non-existing script

def runtests():
    sc = JavaExecutable(TEST_SCRIPT)
    #print(sc.environ)
    print("Executing '{}'...".format(sc.command))
    print(str(sc))
    rc, output = sc.execute()
    print("OUTPUT:\n'{}'".format(output))
    print("RC={}".format(rc))
    print("########## args test")
    sc = JavaExecutable(TEST_SCRIPT)
    print("Executing '{}'...".format(sc.command))
    print(str(sc))
    rc, output = sc.execute("arg1 arg2 arg3")
    print("OUTPUT:\n'{}'".format(output))
    print("RC={}".format(rc))
    print("########## real args test")
    sc = JavaExecutable(TEST_SCRIPT)
    print(sc.command)
    print("Executing...")
    rc, output = sc.execute()
    print(str(sc))
    print("OUTPUT:\n'{}'".format(output))
    print("RC={}".format(rc))
    print("########## non-existing script")
    sc = JavaExecutable(NO_SCRIPT)
    print("Executing '{}'...".format(sc.command))
    rc, output = sc.execute()
    print(str(sc))
    print("OUTPUT:\n'{}'".format(output))
    print("RC={}".format(rc))

if __name__ == "__main__":
    print __doc__
    runtests()

