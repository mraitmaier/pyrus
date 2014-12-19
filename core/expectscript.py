"""
   expectscript.py - expect script implementing the ExpectScript class

   This class is used to run Expect scripts from expect.

   NOTE: This script is not to be run standalone (except for the testing
         purposes), it is meant to be used a module.
"""
# HISTORY ####################################################################
#
#   1   ?????   MR  Initial version
#   2   Dec14   MR  Ported to Py3
#
##############################################################################
__description__ = "a ExpectScript class implementation"
__version__ = "2"
__author__ = "Miran R."

import os
from pyrus.core.executable import Executable

# executing Expect scripts differs on Windows and POSIX platforms
# On Windows, expect is only a TCL extension, while on POSIX is standalone
# executable
import sys
_PLATFORM = sys.platform
if _PLATFORM in ["win32", "cli"]:
    _EXECUTABLE = "tclsh"
else:
    _EXECUTABLE = "expect"

class ExpectScript(Executable):
    """
        ExpectScript - executable wrapper for expect script
    """

    def __init__(self, script):
        super(ExpectScript, self).__init__(script)

    def execute(self, args=""):
        """Executes the Expect script"""
        return super(ExpectScript, self).execute(_EXECUTABLE, args)
#        rc = 1
#        output = ""
#        # check if executable even exists; if so, execute it; otherwise fail
#        if self._checkScript():
#            cmdlist = [_EXECUTABLE, self.command]
#            if args is not None:
#                cmdlist.extend(args.split())
#            # execute it
#            try:
#                proc = Popen(cmdlist, env=self.environ,
#                                      stdin=PIPE, stdout=PIPE, stderr=STDOUT)
#                (output, errors) = proc.communicate()
#                rc = proc.returncode
#            except WindowsError as werror:
#                output = self._ExeError(_EXECUTABLE, werror)
#        else:
#            output = self._ScriptError()
#        return (rc, output)

# TESTING ###################################################################

if _PLATFORM in ["win32", "cli"]:
    TEST_SCRIPT = "test/scripts/test_expect_win.tcl"
    NO_SCRIPT = "test/scripts/tst_expect_win.tcl"
else:
    TEST_SCRIPT = "test/scripts/test.exp"
    NO_SCRIPT = "test/scripts/tst_expect_win.tcl"

def runtests():
    sc = ExpectScript(TEST_SCRIPT)
    print((sc.environ))
    print(("Executing '{}'...".format(sc.command)))
    print((str(sc)))
    rc, output = sc.execute()
    print(("OUTPUT:\n'{}'".format(output)))
    print(("RC={}".format(rc)))
    print("########## args test")
    sc = ExpectScript(TEST_SCRIPT)
    print(("Executing '{}'...".format(sc.command)))
    print((str(sc)))
    rc, output = sc.execute("arg1 arg2 arg3")
    print(("OUTPUT:\n'{}'".format(output)))
    print(("RC={}".format(rc)))
    print("########## real args test")
    sc = ExpectScript(TEST_SCRIPT)
    print((sc.command))
    print("Executing...")
    rc, output = sc.execute()
    print((str(sc)))
    print(("OUTPUT:\n'{}'".format(output)))
    print(("RC={}".format(rc)))
    print("########## non-existing script")
    sc = ExpectScript(NO_SCRIPT)
    print(("Executing '{}'...".format(sc.command)))
    rc, output = sc.execute()
    print((str(sc)))
    print(("OUTPUT:\n'{}'".format(output)))
    print(("RC={}".format(rc)))


if __name__ == "__main__":
    print(__doc__)
    runtests()

