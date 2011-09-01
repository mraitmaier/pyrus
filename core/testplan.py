"""
   testplan.py - 

   NOTE: this module should not be run as a standalone scripts, excepts for
   built-in tests.

"""
# HISTORY ####################################################################
#                       
# 0.0.1     Apr11   MR # This is just an example hot to write history notes
#                       
##############################################################################
from __future__ import print_function

__description__ = "TestPlan class implementation"
__version__ = "0.0.1"
__author__ = "Miran R."

import json
import StringIO
from testable import _Testable
from action import ScriptedAction, NoOpAction, ManualAction, ActionJsonDecoder
from configuration import Configuration, ConfigJsonDecoder
from sut import SystemUnderTest
from testcase import TestCase
from teststep import TestStep

class TestPlan(_Testable):
    """
        TestPlan -
    """

    def __init__(self, name, setup=None, cleanup=None, configs=None):
        assert name is not None
        super(TestPlan, self).__init__(name, setup, cleanup)
        self._cfgs = configs if configs is not None else []

    def __str__(self):
        s = "\n".join(("test plan: {}". format(self.name),
                       "  setup={}".format(str(self.setup)),
                       "  cleanup={}".format(str(self.cleanup)),
                       "  configs={}".format([str(s) for s in self.configs]),
                       ))
        return s

    @property
    def configs(self):
        return self._cfgs

    def addConfig(self, case):
        assert isinstance(case, Configuration)
        self._cfgs.append(case)

    def toJson(self):
        """ """
        return json.dumps(self, cls=_TestPlanJsonEncoder, indent=4)

    def toText(self):
        """ """
        pass

    def toXml(self):
        """ """
        n = """<TestPlan name="{}">""".format(self.name)
        s = "<Setup>\n{}</Setup>".format(self.setup.toXml())
        c = "<Cleanup>\n{}</Cleanup>".format(self.cleanup.toXml())
        cfgs = reduce(lambda x,y: "\n".join((x, y)),
                  [cfg.toXml() for cfg in self.configs])
        return "\n".join((n, s, c, cfgs, "</TestPlan>\n")) 

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
            d["setup"] = obj.setup.toJson()
            d["cleanup"] = obj.cleanup.toJson()
            d["configurations"] = [i.toJson() for i in obj.configs]
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
        cfgs = None
        if "name" in tsDict:
            name = tsDict["name"]
        if "setup" in tsDict:
            setup = ActionJsonDecoder().decode(tsDict["setup"]) 
        if "cleanup" in tsDict:
            cleanup = ActionJsonDecoder().decode(tsDict["cleanup"]) 
        if "configurations" in tsDict:
            cfgs=[]
            for c in tsDict["configurations"]:
                cfgs.append(ConfigJsonDecoder().decode(c)) 
        assert cfgs is not None, "Test plan needs a configuration or two..."
        return TestPlan(name, setup, cleanup, cfgs)
        
# TESTING ####################################################################
FILENAME = "test/testset.json"

def runtests():
    print( "Starting unit tests...")
    ts = TestPlan("a testplan ")
    print(str(ts))
    print(ts.toJson())
    print()
    # add some setup and cleanup actions
    a1 = ScriptedAction("/this/is/a/script/path", "arg1")
    a2 = ScriptedAction("/this/is/a/different/script/path", "arg1 arg2")
    ts.setup = a1
    ts.cleanup = a2
    print(str(ts))
    print()
    # add some configurations
    # add SUT
    _sut = SystemUnderTest("SUT-name", suttype=1, ip="129.234.23.233",
            version="1.0", description="A short description")
    cfg1 = Configuration("the first cfg", sut=_sut)
    cfg2 = Configuration("the second cfg", sut=_sut)
    cfg3 = Configuration("the third cfg")
    ts.addConfig(cfg1)
    ts.addConfig(cfg2)
    ts.addConfig(cfg3)
    print(str(ts))
    print()
    # add some setup and cleanup actions
    cfg1.setup = a1
    cfg1.cleanup = a2
    cfg2.setup = a1
    cfg3.cleanup = a2
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
    cfg1.addTestCase(c1)
    cfg1.addTestCase(c2)
    cfg1.addTestCase(c3)
    cfg2.addTestCase(c3)
    cfg2.addTestCase(c2)
    cfg2.addTestCase(c1)
    cfg3.addTestCase(c2)
    cfg3.addTestCase(c1)
    cfg3.addTestCase(c3)
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
