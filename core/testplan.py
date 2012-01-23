"""
   testplan.py - 

   NOTE: this module should not be run as a standalone scripts, excepts for
   built-in tests.

"""
# HISTORY ####################################################################
#                       
# 0.0.1     Apr11   MR # initial version
# 0.0.2     Jan12   MR # simplification: Configurations are no-more; test plan
#                        carries the list of test cases
#                       
##############################################################################
from __future__ import print_function

__description__ = "TestPlan class implementation"
__version__ = "0.0.2"
__author__ = "Miran R."

import json
import StringIO
from testable import _Testable
from action import AutomatedAction, NoOpAction, ManualAction, ActionJsonDecoder
from sut import SystemUnderTest, SutJsonDecoder
from testcase import TestCase, TestCaseJsonDecoder
from teststep import TestStep

class TestPlan(_Testable):
    """
        TestPlan -
    """

    def __init__(self, name, setup=None, cleanup=None, cases=None, sut=None):
        assert name is not None
        super(TestPlan, self).__init__(name, setup, cleanup)
        self._cases = cases if cases is not None else []
        self._sut = sut if sut is not None else SystemUnderTest("empty SUT")

    def __str__(self):
        s = "\n".join(("test plan: {}". format(self.name),
                       "  setup={}".format(str(self.setup)),
                       "  cleanup={}".format(str(self.cleanup)),
                       "  cases={}".format([str(s) for s in self.testcases]),
                       ))
        return s

    @property
    def testcases(self):
        return self._cases

    @property
    def systemUnderTest(self):
        return self._sut

    def addTestCase(self, case):
        assert isinstance(case, TestCase)
        self._cases.append(case)

    def toJson(self):
        """ """
        return json.dumps(self, cls=_TestPlanJsonEncoder, indent=4)

    def toText(self):
        """ """
        pass

    def toXml(self):
        """ """
        sut = self.systemUnderTest.toXml()
        n = """<TestPlan name="{}">""".format(self.name)
        s = "<Setup>\n{}</Setup>".format(self.setup.toXml())
        c = "<Cleanup>\n{}</Cleanup>".format(self.cleanup.toXml())
        cases = reduce(lambda x,y: "\n".join((x, y)),
                  [case.toXml() for case in self.testcases])
        return "\n".join((n, sut, s, c, cases, "</TestPlan>\n")) 

    def writeJson(self, filename):
        """ """
        assert filename is not None
        fout = open(filename, "w")
        json.dump(self, fout, cls=_TestPlanJsonEncoder, indent=4)
        fout.close()

class _TestPlanJsonEncoder(json.JSONEncoder):
    """Custom JSON encoder for TestPlan class"""

    def default(self, obj):
        if isinstance(obj, TestPlan):
            d = dict()
            d["name"] = obj.name
            d["SUT"] = obj.systemUnderTest.toJson()
            d["setup"] = obj.setup.toJson()
            d["cleanup"] = obj.cleanup.toJson()
            d["testcases"] = [i.toJson() for i in obj.testcases]
            return d
        return json.JSONEncoder.default(self, obj)

class TestPlanJsonDecoder(json.JSONDecoder):
    """Custom JSON decoder for the TestPlan class"""

    def decode(self, jsontext):
        tsDict = json.loads(jsontext)
        #
        name = "Untitled Test Plan"
        setup = []
        cleanup = []
        cases = None
        if "name" in tsDict:
            name = tsDict["name"]
        if "setup" in tsDict:
            setup = ActionJsonDecoder().decode(tsDict["setup"]) 
        if "cleanup" in tsDict:
            cleanup = ActionJsonDecoder().decode(tsDict["cleanup"]) 
        if "SUT" in tsDict:
            sut = SutJsonDecoder().decode(tsDict["SUT"])
        if "testcases" in tsDict:
            cases=[]
            for c in tsDict["testcases"]:
                cases.append(TestCaseJsonDecoder().decode(c)) 
        assert cases is not None, "Test plan needs a test case or two..."
        return TestPlan(name, setup, cleanup, cases)
        
# TESTING ####################################################################
FILENAME = "test/testset.json"

def runtests():
    print( "Starting unit tests...")
    ts = TestPlan("a testplan ")
    print(str(ts))
    print(ts.toJson())
    print()
    # add some setup and cleanup actions
    a1 = AutomatedAction("/this/is/a/script/path", "arg1")
    a2 = AutomatedAction("/this/is/a/different/script/path", "arg1 arg2")
    ts.setup = a1
    ts.cleanup = a2
    print(str(ts))
    print()
    # add some test steps
    s1 = TestStep("the first step")
    s2 = TestStep("the second step")
    s3 = TestStep("the third step")
    # add some test steps
    c1 = TestCase("the first case")
    c2 = TestCase("the second case")
    c3 = TestCase("the third case")
    c1.Setup = a1 
    c1.Cleanup = a2 
    c2.Setup = a2 
    c2.Cleanup = a2 
    c3.Setup = a1 
    c3.Cleanup = a1 
    c1.addStep(s1)
    c1.addStep(s2)
    c1.addStep(s3)
    c2.addStep(s3)
    c2.addStep(s2)
    c2.addStep(s1)
    c3.addStep(s3)
    #
    ts.addTestCase(c1)
    ts.addTestCase(c2)
    ts.addTestCase(c3)
    ts.addTestCase(c3)
    ts.addTestCase(c2)
    ts.addTestCase(c1)
    ts.addTestCase(c2)
    ts.addTestCase(c1)
    ts.addTestCase(c3)
    print(str(ts))
    print()
    j = ts.toJson()
    print(j)
    c = TestPlanJsonDecoder().decode(j)
    print("type: {}\ndata='{}'".format(type(c), str(c)))
    ts.writeJson(FILENAME)
    print("XML={}".format(ts.toXml()))
    print("Stop.")

if __name__ == '__main__':
   print(__doc__)
   runtests()
