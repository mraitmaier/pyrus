"""
   perlscript.py - python script implementing the PerlScript class

   This class is used to run perl scripts from python.

   NOTE: This script is not to be run standalone (except for the testing
         purposes), it is meant to be used a module.
"""
# HISTORY ####################################################################
#
#   1   Dec11   MR  Initial version
#   2   Dec14   MR  Ported to Py3
#
##############################################################################
__description__ = "a PerlScript class implementation"
__version__ = "2"
__author__ = "Miran R."

import os
from pyrus.core.executable import Executable

_EXECUTABLE = "perl"

class PerlScript(Executable):
    """
        PerlScript - executable wrapper for python script
    """

    def __init__(self, script):
        super(PerlScript, self).__init__(script)

    def execute(self, args=""):
        """Executes the Perl script"""
        return super(PerlScript, self).execute(_EXECUTABLE, args)

# TESTING ###################################################################
TEST_SCRIPT = "test/scripts/test.pl"   # existing script
NO_SCRIPT = "test/scripts/tst.pl"      # non-existing script

def runtests():
    sc = PerlScript(TEST_SCRIPT)
    print((sc.environ))
    print(("Executing '{}'...".format(sc.command)))
    print((str(sc)))
    rc, output = sc.execute()
    print(("OUTPUT:\n'{}'".format(output)))
    print(("RC={}".format(rc)))
    print("########## args test")
    sc = PerlScript(TEST_SCRIPT)
    print(("Executing '{}'...".format(sc.command)))
    print((str(sc)))
    rc, output = sc.execute("arg1 arg2 arg3")
    print(("OUTPUT:\n'{}'".format(output)))
    print(("RC={}".format(rc)))
    print("########## real args test")
    sc = PerlScript(TEST_SCRIPT)
    print((sc.command))
    print("Executing...")
    rc, output = sc.execute()
    print((str(sc)))
    print(("OUTPUT:\n'{}'".format(output)))
    print(("RC={}".format(rc)))
    print("########## non-existing script")
    sc = PerlScript(NO_SCRIPT)
    print(("Executing '{}'...".format(sc.command)))
    rc, output = sc.execute()
    print((str(sc)))
    print(("OUTPUT:\n'{}'".format(output)))
    print(("RC={}".format(rc)))


if __name__ == "__main__":
    print(__doc__)
    runtests()

