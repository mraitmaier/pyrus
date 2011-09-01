"""
   requirement.py - 

   NOTE: this module should not be run as a standalone scripts, excepts for
   built-in tests.

"""
# HISTORY ####################################################################
#                       
# 0.0.1     Mar11   MR # This is just an example hot to write history notes
#                       
##############################################################################
from __future__ import print_function

__description__ = "a requirement class implementation"
__version__ = "0.0.1"
_author__ = "Miran R."

import json
from priority import Priority

class RequirementStatus(object):
    """
    """
    ERROR = -1
    NEW = 0
    ACKNOWLEDGED = 1
    PENDING = 2
    APPROVED = 3
    REJECTED = 4
    UNKNOWN = 5

    def __init__(self, val=NEW):
        self._val = val

    def __str__(self):
        if self._val == self.NEW:
            return "new"
        elif self._val == self.ACKNOWLEDGED:
            return "acknowledged"
        elif self._val ==  self.PENDING:
            return "pending"
        elif self._val ==   self.APPROVED:
            return "approved"
        elif self._val ==   self.REJECTED:
            return "rejected"
        elif self._val ==   self.UNKNOWN:
            return "unknown"
        else:
            return "error"
       
class TestableStatus(object):
    """
    """
    ERROR = -1
    VALID = 0
    NOT_TESTABLE = 1
    
    @staticmethod
    def strToVal(strVal):
        assert isinstance(strVal, (str, unicode)), "Must be string...."
        assert strVal is not None
        strVal = strVal.lower().strip()
        if strVal == "valid":
            return TestableStatus.VALID
        elif strVal in ["not testable", "not_testable", "not_test"]:
            return TestableStatus.NOT_TESTABLE
        else:
            return TestableStatus.ERROR

class Requirement(object):
    """ 
        Requirement
    """
    def __init__(self, name, short="", description="",
                             status=RequirementStatus(RequirementStatus.NEW),
                             test_status=TestableStatus.VALID, 
                             priority=Priority.MEDIUM):
        assert name is not None
        self._name = name
        self._short = short
        self._desc = description
        self._status = status
        self._test_status = test_status
        self._prty = priority

    def __str__(self):
        s = "\n".join(("Requirement: {}".format(self.name),
                       "  short: {}".format(self.shortName),
                       "  priority: {}".format(self.priority),
                       "  status: {}".format(self.priority),
                       "  teststatus: {}".format(self.testStatusToString()),
                       "  description:\n{}".format(self.description)
                       ))
        return s

    @property
    def name(self):
        return self._name

    @property
    def shortName(self):
        return self._short

    @property
    def description(self):
       return self._desc

    @property
    def status(self):
       return self._status

    @property
    def testStatus(self):
        return self._test_status

    @property
    def priority(self):
        return self._prty

    def testStatusToString(self):
        """ """
        if self.testStatus == TestableStatus.VALID:
            return "valid"
        elif self.testStatus == TestableStatus.NOT_TESTABLE:
            return "not testable"
        else:
            return "error"
    def toJson(self):
        return json.dumps(self, indent=4, cls=_RequirementJsonEncoder)

class _RequirementJsonEncoder(json.JSONEncoder):
    """Custom JSON encoder for Requirement class"""

    def default(self, obj):
        if isinstance(obj, Requirement):
            d = dict()
            d["name"] = obj.name
            d["short"] = obj.shortName
            d["description"] = obj.description
            d["priority"] = Priority.valToStr(obj.priority)
            d["testStatus"] = obj.testStatusToString()
            d["reqStatus"] = str(obj.status)
            return d
        return json.JSONEncoder(obj)

class RequirementJsonDecoder(json.JSONDecoder):
    """Custom JSON decoder for Requirement class"""
       
    def __statusToVal(self, strVal):
        assert strVal is not None
        strVal = strVal.lower().strip()
        if strVal == "new":
            return RequirementStatus.NEW
        elif strVal == "unknown":
            return RequirementStatus.UNKNOWN
        elif strVal == "approved":
            return RequirementStatus.APPROVED
        elif strVal == "pending":
            return RequirementStatus.PENDING
        elif strVal == "acknowlwdged":
            return RequirementStatus.ACKNOWLEDGED
        elif strVal == "rejected":
            return RequirementStatus.REJECTED
        else:
            return RequirementStatus.ERROR

    def decode(self, jsontext):
        d = json.loads(jsontext)
        #
        name = None
        short = ""
        desc = ""
        pri = Priority.ERROR
        status = RequirementStatus.UNKNOWN
        tstatus = None
        if "name" in d:
            name = d["name"]
        if "short" in d:
            short = d["short"]
        if "description" in d:
            desc = d["description"]
        if "priority" in d:
            pri = Priority.strToVal(d["priority"])
        if "status" in d:
            status = self.__statusToVal(d["status"])
        if "testStatus" in d:
            tstatus = TestableStatus.strToVal(d["testStatus"])
        assert name is not None, "Requirement needs a name..."
        assert pri is not None, "Requirement needs a priority..."
        return Requirement(name, short, desc, status, tstatus, pri)

# TESTING ####################################################################
def test_TestableStatus():
    print("### TestableStatus ###")
    s = TestableStatus.VALID
    print(str(s))
    s = TestableStatus.NOT_TESTABLE
    print(str(s))
    s = TestableStatus.ERROR
    print(str(s))
    st = {"valid":0, "VALID":0, " Valid    ":0, "NOT_TESTABLE":1, 
          "not testable":1, "error":-1, "ERROR":-1, "someti":-1 }
    for key, val in st.items():
        print("Trying '{}'...".format(key))
        res = TestableStatus.strToVal(key)
        if res != val:
            print("FAIL")
            continue
        print("PASS")
    print("Trying invalid val: 666...")
    try:
        TestableStatus.strToVal(666)
    except AssertionError:
        print("Assertion caught: PASS")
    else:
        print("Assertion not caught: FAIL")

def test_RequirementStatus():
    print("### RequirementStatus ###")
    r = RequirementStatus(RequirementStatus.NEW)
    print(str(r))
    r = RequirementStatus(RequirementStatus.ERROR)
    print(str(r))
    r = RequirementStatus(RequirementStatus.ACKNOWLEDGED)
    print(str(r))
    r = RequirementStatus(RequirementStatus.PENDING)
    print(str(r))
    r = RequirementStatus(RequirementStatus.APPROVED)
    print(str(r))
    r = RequirementStatus(RequirementStatus.UNKNOWN)
    print(str(r))
    r = RequirementStatus(RequirementStatus.REJECTED)
    print(str(r))

def test_Requirement():
    print("### Requirement ###")
    r = Requirement("A Requirement name", "short", "Requirement description")
    print(str(r))
    j = r.toJson()
    print(j)
    blah = RequirementJsonDecoder().decode(j)
    print(str(blah))

def runtests():
    test_TestableStatus()
    test_RequirementStatus() 
    test_Requirement()

if __name__ == "__main__":
    print(__doc__)
    runtests()
