"""
   tclscript.py - python script implementing the TclScript class

   This class is used to run tcl scripts from python.

   NOTE: This script is not to be run standalone (except for the testing
         purposes), it is meant to be used a module.
"""
# HISTORY ####################################################################
#
#   1   Dec11   MR Initial version
#   2   Dec14   MR Ported to Py3
#
##############################################################################
__description__ = "a TclScript class implementation"
__version__ = "3"
__author__ = "Miran R."

import os
from pyrus.core.executable import Executable

_EXECUTABLE = "tclsh"

class TclScript(Executable):
    """
        TclScript - executable wrapper for python script
    """

    def __init__(self, script):
        super(TclScript, self).__init__(script)

    def execute(self, args=""):
        """Executes the Tcl script"""
        return super(TclScript, self).execute(_EXECUTABLE, args)

# TESTING ###################################################################
TEST_SCRIPT = "test/scripts/test.tcl"   # existing script
NO_SCRIPT = "test/scripts/tst.tcl"      # non-existing script

def runtests():
    sc = TclScript(TEST_SCRIPT)
    print((sc.environ))
    print(("Executing '{}'...".format(sc.command)))
    print((str(sc)))
    rc, output = sc.execute()
    print(("OUTPUT:\n'{}'".format(output)))
    print(("RC={}".format(rc)))
    print("########## args test")
    sc = TclScript(TEST_SCRIPT)
    print(("Executing '{}'...".format(sc.command)))
    print((str(sc)))
    rc, output = sc.execute("arg1 arg2 arg3")
    print(("OUTPUT:\n'{}'".format(output)))
    print(("RC={}".format(rc)))
    print("########## real args test")
    sc = TclScript(TEST_SCRIPT)
    print((sc.command))
    print("Executing...")
    rc, output = sc.execute()
    print((str(sc)))
    print(("OUTPUT:\n'{}'".format(output)))
    print(("RC={}".format(rc)))
    print("########## non-existing script")
    sc = TclScript(NO_SCRIPT)
    print(("Executing '{}'...".format(sc.command)))
    rc, output = sc.execute()
    print((str(sc)))
    print(("OUTPUT:\n'{}'".format(output)))
    print(("RC={}".format(rc)))


if __name__ == "__main__":
    print(__doc__)
    runtests()

