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
from priority import Priority, toPriority
from enum import enum

RequirementStatus = enum(("NEW", "ACKNOWLEDGED", "PENDING", "APPROVED",
                          "REJECTED", "UNKNOWN", "ERROR"))

def toRequirementStatus(strval):
    """ """
    strval = strval.upper()
    if strval in ["NEW", "N"]:
        return RequirementStatus.NEW
    elif strval in ["ACKNOWLEDGED", "ACK"]:
        return RequirementStatus.ACKNOWLEDGED
    elif strval in ["PENDING", "PEN"]:
        return RequirementStatus.PENDING
    elif strval in ["APPROVED", "APR"]:
        return RequirementStatus.APPROVED
    elif strval in ["REJECTED", "REJ"]:
        return RequirementStatus.REJECTED
    elif strval in ["UNKNOWN", "UNK"]:
        return RequirementStatus.UNKNOWN
    else:
        return RequirementStatus.ERROR

      
TestableStatus = enum(("VALID", "NOT_TESTABLE", "ERROR"))

def toTestableStatus(strval):
    """ """
    strval = strval.upper()
    if strval in ["VALID", "VAL"]:
        return TestableStatus.VALID
    elif strval in ["NOT_TESTABLE", "NOT"]:
        return TestableStatus.NOT_TESTABLE
    else:
        return TestableStatus.ERROR

class Requirement(object):
    """ 
        Requirement
    """
    def __init__(self, name, short="", description="",
                             status=RequirementStatus.NEW,
                             test_status=TestableStatus.VALID, 
                             priority=Priority.MEDIUM, changelog=""):
        assert name is not None
        self._name = name
        self._short = short
        self._desc = description
        self._status = status
        self._test_status = test_status
        self._prty = priority
        self._changelog = changelog

    def __str__(self):
        s = "\n".join(("Requirement: {}".format(self.name),
                       "  short: {}".format(self.shortName),
                       "  priority: {}".format(self.priority),
                       "  status: {}".format(self.status),
                       "  teststatus: {}".format(self.testStatus),
                       "  description:\n{}".format(self.description),
                       "  changelog:\n{}".format(self.changelog)
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

    @property
    def changelog(self):
        return self._changelog

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
            d["priority"] = obj.priority
            d["testStatus"] = obj.testStatus
            d["reqStatus"] = str(obj.status)
            d["changelog"] = obj.changelog
            return d
        return json.JSONEncoder(obj)

class RequirementJsonDecoder(json.JSONDecoder):
    """Custom JSON decoder for Requirement class"""
       
    def decode(self, jsontext):
        d = json.loads(jsontext)
        #
        name = None
        short = ""
        desc = ""
        pri = Priority.ERROR
        status = RequirementStatus.UNKNOWN
        tstatus = None
        log = ""
        if "name" in d:
            name = d["name"]
        if "short" in d:
            short = d["short"]
        if "description" in d:
            desc = d["description"]
        if "priority" in d:
            pri = toPriority(d["priority"])
        if "status" in d:
            status = toRequirementStatus(d["status"])
        if "testStatus" in d:
            tstatus = toTestableStatus(d["testStatus"])
        if "changelog" in d:
            log = d["changelog"]
        assert name is not None, "Requirement needs a name..."
        assert pri is not None, "Requirement needs a priority..."
        return Requirement(name, short, desc, status, tstatus, pri, log)

# TESTING ####################################################################
def test_TestableStatus():
    print("### TestableStatus ###")
    s = TestableStatus.VALID
    print(str(s))
    s = TestableStatus.NOT_TESTABLE
    print(str(s))
    s = TestableStatus.ERROR
    print(str(s))

def test_RequirementStatus():
    print("### RequirementStatus ###")
    r = RequirementStatus.NEW
    print(str(r))
    r = RequirementStatus.ERROR
    print(str(r))
    r = RequirementStatus.ACKNOWLEDGED
    print(str(r))
    r = RequirementStatus.PENDING
    print(str(r))
    r = RequirementStatus.APPROVED
    print(str(r))
    r = RequirementStatus.UNKNOWN
    print(str(r))
    r = RequirementStatus.REJECTED
    print(str(r))

def test_Requirement():
    print("### Requirement ###")
    r = Requirement("A Requirement name", "short", "Requirement description")
    print(str(r))
    j = r.toJson()
    print(j)
    blah = RequirementJsonDecoder().decode(j)
    print(str(blah))
    r2 = Requirement("A different Requirement name", "short", 
            "A Different Requirement description", priority=Priority.HIGH)
    print(str(r2))
    j2 = r2.toJson()
    print(j2)
    blah = RequirementJsonDecoder().decode(j2)
    print(str(blah))

def runtests():
    test_TestableStatus()
    test_RequirementStatus() 
    test_Requirement()

if __name__ == "__main__":
    print(__doc__)
    runtests()
