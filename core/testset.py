"""
   testset.py - 

   NOTE: this module should not be run as a standalone scripts, excepts for
   built-in tests.

"""
# HISTORY ####################################################################
#                       
#   1   Mar11   MR # initial version
#   2   Jan12   MR # simplification: Configuration is no-more, TestSet contains list of TestCase-s 
#   2   Dec14   MR # ported to Py3
#                       
##############################################################################

__description__ = "TestSet class implementation"
__version__ = "3"
__author__ = "Miran R."

import json
import io
from pyrus.core.runnable import Runnable
from pyrus.core.testplan import TestPlan
from pyrus.core.action import ActionJsonDecoder
from pyrus.core.testcase import TestCaseJsonDecoder
from pyrus.core.teststatus import TestStatus
from pyrus.core.sut import SystemUnderTest, SutJsonDecoder
from functools import reduce

class TestSet(TestPlan, Runnable):
    """
        TestSet -
    """

    def __init__(self, name, testplan, setup=None, cleanup=None, cases=None, sut=None):
        assert name is not None
        super(TestSet, self).__init__(name, setup, cleanup)
        # a list of configurations
        self._cases = cases if cases is not None else [] 
        self._plan = testplan # a testplan name to which set is connected
        self._sut = sut if sut is not None else SystemUnderTest("Empty SUT")

    def __str__(self):
        s = "\n".join(("test set: {}".format(self.name),
                       "  belongs to '{}'".format(self._plan),
                       "  {}".format(str(self._sut)),
                       "  setup={}".format(str(self.setup)),
                       "  cleanup={}".format(str(self.cleanup)),
                       "  cases={}".format([str(s) for s in self.testcases]),
                       ))
        return s

    @property
    def testplan(self):
        return self._plan

    @property
    def systemUnderTest(self):
        return self._sut

    def toJson(self):
        """ """
        return json.dumps(self, cls=_TestSetJsonEncoder, indent=4)

    def toText(self):
        """ """
        pass

    def toXml(self):
        """ """
        sut = self.systemUnderTest.toXml()
        n = """<TestSet name="{}">""".format(self.name)
        p = "<TestPlan>{}</TestPlan>".format(self.testplan)
        s = "<Setup>\n{}</Setup>".format(self.setup.toXml())
        c = "<Cleanup>\n{}</Cleanup>".format(self.cleanup.toXml())
        cases = reduce(lambda x,y: "\n".join((x, y)), [case.toXml() for case in self.testcases])
        return "\n".join((n, p, sut, s, c, cases, "</TestSet>\n"))

    def toHtml(self, short=True, cssClass=None):
        """Return a HTML representation of the class"""
        if short:
           return self._shortHtml(cssClass)
        return self._longHtml(cssClass)   

    def _shortHtml(self, cssClass):       
        sStatus = TestStatus.PASS if self.setup.returncode == 0 else TestStatus.FAIL
        cStatus = TestStatus.PASS if self.cleanup.returncode == 0 else TestStatus.FAIL
        if cssClass:
            d = """<div id="testset" class="{}">""".format(cssClass)
        else:
            d = """<div id="testset">"""
        h = "<h1>Test Set: {}</h1>".format(self.name)
        p = "<p>This test set is related to <b>{}</b> test plan.</p>".format(self.testplan)
        s = "<table><tr><td>Setup</td><td>{}</td><td>{}</td></tr>".format(self.setup.toHtml(), sStatus)
        c = "<tr><td>Cleanup</td><td>{}</td><td>{}</td></tr></table>".format(self.cleanup.toHtml(), cStatus)
        cases = reduce(self.__join, [case.toHtml(True) for case in self.testcases])
        return "\n".join((d, h, p, s, c, cases,"</div>"))

    def _longHtml(self, cssClass):       
        if cssClass:
            d = """<div id="testset" class="{}">""".format(cssClass)
        else:
            d = """<div id="testset">"""
        h = "<h1>Test Set: {}</h1>".format(self.name)
        p = "This test set is related to <b>{}</b> test plan.<br>".format(self.testplan)
        s = "<p>Setup: {}</p>".format(self.setup.toHtml(short=False))
        c = "<p>Cleanup: {}</p>".format(self.cleanup.toHtml(short=False))
        cases = reduce(self.__join, [case.toHtml(False) for case in self.testcases])
        return "\n".join((d, p, h, s, c, cases,"</div>"))
        
    def __join(self, s1, s2):
        return "\n".join((s1, s2))

    def writeJson(self, filename):
        """ """
        assert filename is not None
        fout = open(filename, "w")
        json.dump(self, fout, cls=_TestSetJsonEncoder, indent=4)
        fout.close()

    def execute(self, **kwargs):
        """Overriden method from Runnable mixin."""
        # define indentation level for printouts   
        indent_lvl = 1
        text = io.StringIO()
        text.write("{}\n".format("#"*79))
        text.write("Starting execution of test set: '{}'\n".format(self.name))
        text.write("{}\n".format("#"*79))
        # execute setup actions    
        failed = self._executeSetup(text, indent_lvl, **kwargs)
        # execute cases
        for case in self.testcases:
            if not failed: 
                text.write("\n  >>> Executing test case: '{}'".format(case.name))
                output = case.execute(**kwargs)
                text.write("  ### OUTPUT ###\n{}\n### END ###\n".format(output))
            else:
                text.write("\n  >>> Configuration '{}' SKIPPED)\n".format(case.name))
        # execute cleanup actions    
        self._executeCleanup(text, indent_lvl, failed, **kwargs)
        text.write("{}\n".format("#"*79))
        text.write("Execution of test set '{}' ended\n".format(self.name))
        text.write("{}\n".format("#"*79))
        return text.getvalue()

class _TestSetJsonEncoder(json.JSONEncoder):
    """Custom JSON encoder for TestSet class"""

    def default(self, obj):
        if isinstance(obj, TestSet):
            d = dict()
            d["name"] = obj.name
            d["testplan"] = obj.testplan
            d["SUT"] = obj.systemUnderTest.toJson()
            d["setup"] = obj.setup.toJson()
            d["cleanup"] = obj.cleanup.toJson()
            d["cases"] = [i.toJson() for i in obj.testcases]
            return d
        return json.JSONEncoder.default(self, obj)

class TestSetJsonDecoder(json.JSONDecoder):
    """Custom JSON decoder for the TestSet class"""

    def decode(self, jsontext):
        tsDict = json.loads(jsontext)
        #
        name = "Untitled Test Set"
        setup = []
        cleanup = []
        cases = None
        testplan = "Unknown test plan"
        if "name" in tsDict:
            name = tsDict["name"]
        if "testplan" in tsDict:
            testplan = tsDict["testplan"]
        if "SUT" in tsDict:
            sut = SutJsonDecoder().decode(tsDict["SUT"])
        if "setup" in tsDict:
            setup = ActionJsonDecoder().decode(tsDict["setup"]) 
        if "cleanup" in tsDict:
            cleanup = ActionJsonDecoder().decode(tsDict["cleanup"]) 
        if "cases" in tsDict:
            cases=[]
            for c in tsDict["cases"]:
                cases.append(TestCaseJsonDecoder().decode(c)) 
        assert testplan is not None
        assert cases is not None, "Test Set needs a configuration or two..."
        return TestSet(name, testplan, setup, cleanup, cases)
        
# TESTING ####################################################################
FILENAME = "test/testset.json"

def runtests():
    print( "Starting unit tests...")
    ts = TestSet("a testset", "an example test plan")
    print(str(ts))
    # add some setup and cleanup actions
    a1 = AutomatedAction("test/scripts/test.py", "arg1")
    a2 = AutomatedAction("test/scripts/hello.jar", "arg1 arg2")
    a3 = AutomatedAction("/this/is/invalid/script/path")
    ts.setup = a1
    ts.cleanup = a2
    # SUT
    _sut = SystemUnderTest("SUT-name", suttype=1, ip="129.234.23.233",
            version="1.0", description="A short description")
    # add some test steps
    s1 = TestStep("the first step")
    s1.action = a1
    s2 = TestStep("the second step")
    s2.action = a2
    s3 = TestStep("the third step")
    s3.action = a3
    # add some test steps
    c1 = TestCase("the first case")
    c2 = TestCase("the second case")
    c3 = TestCase("the third case")
    c1.setup = a1
    c1.cleanup = a2
    c2.setup = a2
    c2.cleanup = a2
    c3.setup = a1
    c3.cleanup = a1
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
    print(str(ts))
    print()
    j = ts.toJson()
    print(j)
##
#    import os
#    fout = open(os.path.abspath("../cfg/example.json"), "w")
#    fout.write(j)
#    fout.close()
##    
    c = TestSetJsonDecoder().decode(j)
    print("type: {}\ndata='{}'".format(type(c), str(c)))
    ts.writeJson(FILENAME)
    print(">>> Executing...")
    out = ts.execute()
    print(">>> OUTPUT\n'{}'\n>>> END".format(out))
    print("XML={}".format(ts.toXml()))
    print("HTML={}".format(ts.toHtml()))
    print("HTML={}".format(ts.toHtml(False)))
    print("Stop.")

if __name__ == '__main__':
    from action import AutomatedAction, NoOpAction 
    from action import ManualAction
    from sut import SystemUnderTest
    from testcase import TestCase
    from teststep import TestStep
    print(__doc__)
    runtests()
