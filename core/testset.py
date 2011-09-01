"""
   testset.py - 

   NOTE: this module should not be run as a standalone scripts, excepts for
   built-in tests.

"""
# HISTORY ####################################################################
#                       
# 0.0.1     Mar11   MR # This is just an example hot to write history notes
#                       
##############################################################################
from __future__ import print_function

__description__ = "TestSet class implementation"
__version__ = "0.0.1"
__author__ = "Miran R."

import json
import StringIO
from runnable import Runnable
from testplan import TestPlan
from action import ActionJsonDecoder
from configuration import ConfigJsonDecoder
from testresult import TestResult

class TestSet(TestPlan, Runnable):
    """
        TestSet -
    """

    def __init__(self, name, testplan, setup=None, cleanup=None, configs=None):
        assert name is not None
        super(TestSet, self).__init__(name, setup, cleanup)
        # a list of configurations
        self._cfgs = configs if configs is not None else [] 
        self._plan = testplan # a testplan name to which set is connected

    def __str__(self):
        s = "\n".join(("test set: {}".format(self.name),
                       "  belongs to '{}'".format(self._plan),
                       "  setup={}".format(str(self.setup)),
                       "  cleanup={}".format(str(self.cleanup)),
                       "  configs={}".format([str(s) for s in self.configs]),
                       ))
        return s

    @property
    def testplan(self):
        return self._plan

    def toJson(self):
        """ """
        return json.dumps(self, cls=_TestSetJsonEncoder, indent=4)

    def toText(self):
        """ """
        pass

    def toXml(self):
        """ """
        n = """<TestSet name="{}">""".format(self.name)
        p = "<TestPlan>{}</TestPlan>".format(self.testplan)
        s = "<Setup>\n{}</Setup>".format(self.setup.toXml())
        c = "<Cleanup>\n{}</Cleanup>".format(self.cleanup.toXml())
        cfgs = reduce(lambda x,y: "\n".join((x, y)),
                    [cfg.toXml() for cfg in self.configs])
        return "\n".join((n, p, s, c, cfgs, "</TestSet>\n"))

    def toHtml(self, short=True, cssClass=None):
        """Return a HTML representation of the class"""
        if short:
           return self._shortHtml(cssClass)
        return self._longHtml(cssClass)   

    def _shortHtml(self, cssClass):       
        sStatus = str(TestResult(self.setup.returncode))
        cStatus = str(TestResult(self.cleanup.returncode))
        if cssClass:
            d = """<div id="testset" class="{}">""".format(cssClass)
        else:
            d = """<div id="testset">"""
        h = "<h1>Test Set: {}</h1>".format(self.name)
        p = "<p>This test set is related to <b>{}</b> test plan.</p>".format(
                self.testplan)
        s = "<table><tr><td>Setup</td><td>{}</td><td>{}</td></tr>".format(
                self.setup.toHtml(), sStatus)
        c = "<tr><td>Cleanup</td><td>{}</td><td>{}</td></tr></table>".format(
                self.cleanup.toHtml(), cStatus)
        cfgs = reduce(self.__join, [cfg.toHtml(True) for cfg in self.configs])
        return "\n".join((d, h, p, s, c, cfgs,"</div>"))

    def _longHtml(self, cssClass):       
        if cssClass:
            d = """<div id="testset" class="{}">""".format(cssClass)
        else:
            d = """<div id="testset">"""
        h = "<h1>Test Set: {}</h1>".format(self.name)
        p = "This test set is related to <b>{}</b> test plan.<br>".format(
                self.testplan)
        s = "<p>Setup: {}</p>".format(self.setup.toHtml(short=False))
        c = "<p>Cleanup: {}</p>".format(self.cleanup.toHtml(short=False))
        cfgs = reduce(self.__join, [cfg.toHtml(False) for cfg in self.configs]) 
        return "\n".join((d, p, h, s, c, cfgs,"</div>"))
        
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
        text = StringIO.StringIO()
        text.write("{}\n".format("#"*79))
        text.write("Starting execution of test set: '{}'\n".format(self.name))
        text.write("{}\n".format("#"*79))
        # execute setup actions    
        failed = self._executeSetup(text, indent_lvl, **kwargs)
        # execute cases
        for cfg in self.configs:
            if not failed: 
                text.write("\n  >>> Executing configuration: '{}'".format(
                                                                     cfg.name))
                output = cfg.execute(**kwargs)
                text.write("  ### OUTPUT ###\n{}\n### END ###\n".format(output))
            else:
                text.write("\n  >>> Configuration '{}' SKIPPED)\n".format(
                                                                     cfg.name))
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
            d["setup"] = obj.setup.toJson()
            d["cleanup"] = obj.cleanup.toJson()
            d["configurations"] = [i.toJson() for i in obj.configs]
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
        cfgs = None
        testplan = "Unknown test plan"
        if "name" in tsDict:
            name = tsDict["name"]
        if "testplan" in tsDict:
            testplan = tsDict["testplan"]
        if "setup" in tsDict:
            setup = ActionJsonDecoder().decode(tsDict["setup"]) 
        if "cleanup" in tsDict:
            cleanup = ActionJsonDecoder().decode(tsDict["cleanup"]) 
        if "configurations" in tsDict:
            cfgs=[]
            for c in tsDict["configurations"]:
                cfgs.append(ConfigJsonDecoder().decode(c)) 
        assert testplan is not None
        assert cfgs is not None, "Test Set needs a configuration or two..."
        return TestSet(name, testplan, setup, cleanup, cfgs)
        
# TESTING ####################################################################
FILENAME = "test/testset.json"

def runtests():
    print( "Starting unit tests...")
    ts = TestSet("a testset", "an example test plan")
    print(str(ts))
    # add some setup and cleanup actions
    a1 = ScriptedAction("test/scripts/test.py", "arg1")
    a2 = ScriptedAction("test/scripts/hello.jar", "arg1 arg2")
    a3 = ScriptedAction("/this/is/invalid/script/path")
    ts.setup = a1
    ts.cleanup = a2
    # SUT
    _sut = SystemUnderTest("SUT-name", suttype=1, ip="129.234.23.233",
            version="1.0", description="A short description")
    # add some test cfgs
    cfg1 = Configuration("the first cfg", sut=_sut)
    cfg2 = Configuration("the second cfg", sut=_sut)
    cfg3 = Configuration("the third cfg")
    ts.addConfig(cfg1)
    ts.addConfig(cfg2)
    ts.addConfig(cfg3)
    # add some setup and cleanup actions
    cfg1.setup = a1
    cfg3.cleanup = a2
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
    cfg1.addTestCase(c1)
    cfg1.addTestCase(c2)
    cfg1.addTestCase(c3)
    cfg2.addTestCase(c3)
    cfg2.addTestCase(c2)
    cfg2.addTestCase(c1)
    cfg3.addTestCase(c1)
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
    from action import ScriptedAction, NoOpAction 
    from action import ManualAction
    from configuration import Configuration
    from sut import SystemUnderTest
    from testcase import TestCase
    from teststep import TestStep
    print(__doc__)
    runtests()
