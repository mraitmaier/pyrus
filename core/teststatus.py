"""
   teststatus.py - a script implementing TestStatus and TestStatus classes

   The former is the main class (as the name of the file suggests...) and it
   is a container for test result. The latter is just a simple helper class
   serving as a enum for available test result values. It's convenient for
   importing and easy to use.

   NOTE: this module should not be run as a standalone scripts, excepts for
   built-in tests.
"""
# HISTORY ####################################################################
#
#  1 Jan12   MR # The initial version of the file
#  2 Dec14   MR # Ported to Py3
#
##############################################################################


__description__ = "TestStatus class implementation"
__version__ = "3"
__author__ = "Miran R."

from pyrus.core.enum import enum

TestStatus = enum(("PASS", "FAIL", "XFAIL", "NOT_TESTED", "UNKNOWN"))

def toTestStatus(str_val):
    """Converts strings to TestStatus values."""
    str_val = str_val.upper()
    if str_val in ["PASS", "PASSED"]:
        return TestStatus.PASS
    elif str_val in ["FAIL", "FAILED"]:
        return TestStatus.FAIL
    elif str_val in ["XFAIL", "EXPECTED_FAIL", "EXPECTED FAIL"]:
        return TestStatus.XFAIL
    elif str_val in ["NOT_TESTED", "NOT TESTED"]:
        return TestStatus.NOT_TESTED
    else:
        return TestStatus.UNKNOWN

def runtests():
    print("#### Starting tests...")
    status = TestStatus.PASS
    print(str(status))
    status = TestStatus.FAIL
    assert TestStatus.NOT_TESTED in TestStatus
    assert "UNKNOWN" in TestStatus
    assert "BLAH" not in TestStatus
    try:
        x = TestStatus.SOMETHING
    except AttributeError as err:
        print("Error caught:", err)
    print("#### repr")
    print(repr(TestStatus))
    print("#### str")
    print(str(TestStatus))
    print("#### Iteration")
    [ print(s) for s in TestStatus ]
    [ print(v) for v in enumerate(TestStatus) ]
    print("#### Stop")
    status = "PASS"

if __name__ == '__main__':
   print(__doc__)
   runtests()
