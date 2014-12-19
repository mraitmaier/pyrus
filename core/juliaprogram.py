"""
   juliaprogram.py - python script implementing the JuliaProgram class

   This class is used to run Julia programs from python.

   NOTE: This script is not to be run standalone (except for the testing
         purposes), it is meant to be used a module.
"""
# HISTORY ####################################################################
#
#   1   Nov13   MR  Initial version
#   2   Dec14   MR  Ported to Py3
#
##############################################################################
__description__ = "a JuliaProgram class implementation"
__version__ = "2"
__author__ = "Miran R."

import os
import sys
from pyrus.core.executable import Executable

if sys.platform in ["win32", "win64"]:
    _EXECUTABLE = ["cmd", "/c", "julia"]
else:
    _EXECUTABLE = "julia"

class JuliaProgram(Executable):
    """
        JuliaProgram - executable wrapper for Lua script
    """

    def __init__(self, script):
        super(JuliaProgram, self).__init__(script)

    def execute(self, args=""):
        """Executes the Julia program"""
        return super(JuliaProgram, self).execute(_EXECUTABLE, args)

# TESTING ###################################################################
TEST_SCRIPT = "test/scripts/test.jl"   # existing script
NO_SCRIPT = "test/scripts/tst.jl"      # non-existing script

def runtests():
    sc = JuliaProgram(TEST_SCRIPT)
    print((sc.environ))
    print(("Executing '{}'...".format(sc.command)))
    print((str(sc)))
    rc, output = sc.execute()
    print(("OUTPUT:\n'{}'".format(output)))
    print(("RC={}".format(rc)))
    print("########## args test")
    sc = JuliaProgram(TEST_SCRIPT)
    print(("Executing '{}'...".format(sc.command)))
    print((str(sc)))
    rc, output = sc.execute("arg1 arg2 arg3")
    print(("OUTPUT:\n'{}'".format(output)))
    print(("RC={}".format(rc)))
    print("########## real args test")
    sc = JuliaProgram(TEST_SCRIPT)
    print((sc.command))
    print("Executing...")
    rc, output = sc.execute()
    print((str(sc)))
    print(("OUTPUT:\n'{}'".format(output)))
    print(("RC={}".format(rc)))
    print("########## non-existing script")
    sc = JuliaProgram(NO_SCRIPT)
    print(("Executing '{}'...".format(sc.command)))
    rc, output = sc.execute()
    print((str(sc)))
    print(("OUTPUT:\n'{}'".format(output)))
    print(("RC={}".format(rc)))

if __name__ == "__main__":
    print(__doc__)
    runtests()

