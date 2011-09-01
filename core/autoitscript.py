"""
   autoitscript.py - autoit script implementing the AutoitScript class

   This class is used to run Autoit scripts from autoit.

   NOTE: This script is not to be run standalone (except for the testing
         purposes), it is meant to be used a module.
"""
# HISTORY ####################################################################
#
# 0.0.1     Mar11   MR  Initial version of the module
##############################################################################
__description__ = "a AutoitScript class implementation"
__version__ = "0.0.1"
__author__ = "Miran R."

import os
from executable import Executable
#from subprocess import Popen, PIPE, STDOUT

import sys
if sys.platform not in ["win32"]:
    print "AutoIt scripts cannot be run on non-Windows systems."
    raise SystemExit

_EXECUTABLE = "autoit3.exe"

class AutoitScript(Executable):
    """
        AutoitScript - executable wrapper for autoit script
    """

    def __init__(self, script):
        super(AutoitScript, self).__init__(script)

    def execute(self, args=""):
        """Executes the Autoit script"""
        return super(AutoitScript, self).execute(_EXECUTABLE, args)
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

def runtests():
    sc = AutoitScript(TEST_SCRIPT)
    print(sc.environ)
    print("Executing '{}'...".format(sc.command))
    print(str(sc))
    rc, output = sc.execute()
    print("OUTPUT:\n'{}'".format(output))
    print("RC={}".format(rc))
    print("########## args test")
    sc = AutoitScript(TEST_SCRIPT)
    print("Executing '{}'...".format(sc.command))
    print(str(sc))
    rc, output = sc.execute("arg1 arg2 arg3")
    print("OUTPUT:\n'{}'".format(output))
    print("RC={}".format(rc))
    print("########## real args test")
    sc = AutoitScript(TEST_SCRIPT)
    print(sc.command)
    print("Executing...")
    rc, output = sc.execute()
    print(str(sc))
    print("OUTPUT:\n'{}'".format(output))
    print("RC={}".format(rc))
    print("########## non-existing script")
    sc = AutoitScript(NO_SCRIPT)
    print("Executing '{}'...".format(sc.command))
    rc, output = sc.execute()
    print(str(sc))
    print("OUTPUT:\n'{}'".format(output))
    print("RC={}".format(rc))


if __name__ == "__main__":
    print __doc__
    runtests()

