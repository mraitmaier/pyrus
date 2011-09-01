"""
   testresult.py - a script implementing TestResult and TestStatus classes

   The former is the main class (as the name of the file suggests...) and it
   is a container for test result. The latter is just a simple helper class
   serving as a enum for available test result values. It's convenient for
   importing and easy to use.

   NOTE: this module should not be run as a standalone scripts, excepts for
   built-in tests.
"""
# HISTORY ####################################################################
#
# 0.0.1     Mar11   MR # The initial version of the file
##############################################################################
__description__ = "TestResult class implementation"
__version__ = "0.0.1"
__author__ = "Miran R."

import json 

class TestStatus(object):
    """
        TestStatus - class representing an values enum for TestResult class 
    """

    UNKNOWN = -1
    PASS = 0
    FAIL = 1 
    XFAIL = 2
    NOT_TESTED = 3
    SKIPPED = 4

    values = [UNKNOWN, PASS, FAIL, XFAIL, NOT_TESTED, SKIPPED]

    @staticmethod
    def convert(strVal):
        """Converts the string representation into proper value"""
        strVal = strVal.strip().lower()
        val = TestStatus.UNKNOWN
        if strVal == "pass":
            val = TestStatus.PASS
        elif strVal == "fail":
            val = TestStatus.FAIL
        elif strVal in ["expected fail", "xfail", "expected_fail"]:
            val = TestStatus.XFAIL
        elif strVal in ["not tested", "not_tested"]:
            val = TestStatus.NOT_TESTED
        elif strVal == "skipped":
            val = TestStatus.SKIPPED
        return val

class TestResult(object):
    """
        TestResult - represents a result of a test that has been run

        It's easy to use and import.
    """

    def __init__(self, val=TestStatus.UNKNOWN):
        self.result = val

    def __str__(self):
        """string representation"""
        if self.result == TestStatus.UNKNOWN:
            s = "unknown"
        elif self.result == TestStatus.PASS:
            s = "pass"
        elif self.result == TestStatus.FAIL:
            s = "fail"
        elif self.result == TestStatus.XFAIL:
            s = "expected fail"
        elif self.result == TestStatus.NOT_TESTED:
            s = "not tested"
        elif self.result == TestStatus.SKIPPED:
            s = "skipped"
        else:
            raise ValueError("Unknown test result value")
        return s
    
    @property
    def result(self):
        """The 'result' property getter"""
        return self._result

    @result.setter
    def result(self, val):
        """The 'result' property setter"""
        assert val in TestStatus.values, "Invalid value: {}".format(val) 
        self._result = val

    def toJson(self):
        return json.dumps(self, cls=_TestResultJsonEncoder)

class _TestResultJsonEncoder(json.JSONEncoder):
    """ """
    def default(self, obj):
        if isinstance(obj, TestResult):
            return { "result": str(obj) }
        return jsonJSONEncoder.default(self, obj)

def runtests():
    print("Starting tests...")
    tr = TestResult(TestStatus.UNKNOWN)
    print(str(tr))
    tr.result = TestStatus.PASS
    print(str(tr))
    tr = TestResult(1)
    print(str(tr))
    print(tr.toJson())
    try:
        tr = TestResult(666)
        print(str(tr))
    except AssertionError as ex:
        print("Assertion error caught: this is OK")
        print(ex)
    print(">>> TestStatus convert tests...")
    print(TestStatus.convert("PASS")  ) 
    print(TestStatus.convert("Pass")  ) 
    print(TestStatus.convert("pass")  ) 
    print(TestStatus.convert("    pAss    "))   
    print(TestStatus.convert("    fail    "))   
    print(TestStatus.convert("xfail    ")  ) 
    print(TestStatus.convert("expected fail"))   
    print(TestStatus.convert("Skipped"))   
    print(TestStatus.convert("not tested"))   
    print(TestStatus.convert("irrelevant"))   
    print("Stop")

if __name__ == '__main__':
   print(__doc__)
   runtests()
