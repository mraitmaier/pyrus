"""
   luascript.py - python script implementing the LuaScript class

   This class is used to run lua scripts from python.

   NOTE: This script is not to be run standalone (except for the testing
         purposes), it is meant to be used a module.
"""
# HISTORY ####################################################################
#   1   Nov13   MR  Initial version
##############################################################################
__description__ = "a LuaScript class implementation"
__version__ = "1"
__author__ = "Miran R."

import os
from executable import Executable

class LuaScript(Executable):
    """
        LuaScript - executable wrapper for Lua script
    """

    def __init__(self, script):
        super(LuaScript, self).__init__(script)

    def execute(self, args=""):
        """Executes the Lua script"""
        return super(LuaScript, self).execute("lua", args)

# TESTING ###################################################################
TEST_SCRIPT = "test/scripts/test.lua"   # existing script
NO_SCRIPT = "test/scripts/tst.lua"      # non-existing script

def runtests():
    sc = LuaScript(TEST_SCRIPT)
    print(sc.environ)
    print("Executing '{}'...".format(sc.command))
    print(str(sc))
    rc, output = sc.execute()
    print("OUTPUT:\n'{}'".format(output))
    print("RC={}".format(rc))
    print("########## args test")
    sc = LuaScript(TEST_SCRIPT)
    print("Executing '{}'...".format(sc.command))
    print(str(sc))
    rc, output = sc.execute("arg1 arg2 arg3")
    print("OUTPUT:\n'{}'".format(output))
    print("RC={}".format(rc))
    print("########## real args test")
    sc = LuaScript(TEST_SCRIPT)
    print(sc.command)
    print("Executing...")
    rc, output = sc.execute()
    print(str(sc))
    print("OUTPUT:\n'{}'".format(output))
    print("RC={}".format(rc))
    print("########## non-existing script")
    sc = LuaScript(NO_SCRIPT)
    print("Executing '{}'...".format(sc.command))
    rc, output = sc.execute()
    print(str(sc))
    print("OUTPUT:\n'{}'".format(output))
    print("RC={}".format(rc))


if __name__ == "__main__":
    print __doc__
    runtests()

