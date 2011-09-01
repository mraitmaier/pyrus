"""
   NativeExecutable.py - java script implementing the NativeExecutable class

   This class is used to run java executables from python.

   NOTE: This script is not to be run standalone (except for the testing
         purposes), it is meant to be used a module.
"""
# HISTORY ####################################################################
# 0.0.1     Mar11   MR  Initial version.
#
##############################################################################
__description__ = "a NativeExecutable class implementation"
__version__ = "0.0.1"
__author__ = "Miran R."

import os
from executable import Executable
from subprocess import Popen, PIPE, STDOUT

class NativeExecutable(Executable):
    """
        NativeExecutable - executable wrapper for java executable
    """

    def __init__(self, script):
        super(NativeExecutable, self).__init__(script)

    def execute(self, args=""):
        """Executes the Native executable"""
        assert args is not None
        rc = 1
        output = ""
        # check if executable even exists; if so, execute it; otherwise fail
        if self._checkScript():
            cmdlist = [self.command]
            if args != "":
                cmdlist.extend(args.split())
            # execute it
            try:
                proc = Popen(cmdlist, env=self.environ,
                                      stdin=PIPE, stdout=PIPE, stderr=STDOUT)
                (output, errors) = proc.communicate()
                rc = proc.returncode
            except OSError as oserror:
                output = self._ExeError(self.command, oserror)
        else:
            output = self._ScriptError()
        return (rc, output)

# TESTING ###################################################################
TEST_SCRIPT = "test/scripts/uname"   # existing script
NO_SCRIPT = "test/scripts/blagh"      # non-existing script

def runtests():
    sc = NativeExecutable(TEST_SCRIPT)
    print(sc.environ)
    print("Executing '{}'...".format(sc.command))
    print(str(sc))
    rc, output = sc.execute()
    print("OUTPUT:\n'{}'".format(output))
    print("RC={}".format(rc))
    print("########## args test")
    sc = NativeExecutable(TEST_SCRIPT)
    print("Executing '{}'...".format(sc.command))
    print(str(sc))
    rc, output = sc.execute("-a")
    print("OUTPUT:\n'{}'".format(output))
    print("RC={}".format(rc))
    print("########## real args test")
    sc = NativeExecutable(TEST_SCRIPT)
    print(sc.command)
    print("Executing...")
    rc, output = sc.execute()
    print(str(sc))
    print("OUTPUT:\n'{}'".format(output))
    print("RC={}".format(rc))
    print("########## non-existing script")
    sc = NativeExecutable(NO_SCRIPT)
    print("Executing '{}'...".format(sc.command))
    rc, output = sc.execute()
    print(str(sc))
    print("OUTPUT:\n'{}'".format(output))
    print("RC={}".format(rc))

if __name__ == "__main__":
    print __doc__
    runtests()

