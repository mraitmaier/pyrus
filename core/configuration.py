"""
   configuration.py - 

   NOTE: this module should not be run as a standalone scripts, excepts for
   built-in tests.

"""
# HISTORY ####################################################################
#                       
# 0.0.1     Mar11   MR # This is just an example hot to write history notes
#                       
##############################################################################
__description__ = "Configuration class implementation"
__version__ = "0.0.1"
__author__ = "Miran R."

import json
import StringIO
from testable import _Testable
from runnable import Runnable
from action import ScriptedAction, NoOpAction, ManualAction, ActionJsonDecoder
from testcase import TestCase, TestCaseJsonDecoder
from sut import SystemUnderTest, SutJsonDecoder
from testresult import TestStatus, TestResult

class Configuration(_Testable, Runnable):
    """
    """

    def __init__(self, name, setup=None, cleanup=None, sut=None, cases=None):
        assert name is not None
        super(Configuration, self).__init__(name, setup, cleanup)
        self._cases = cases if cases is not None else []
        self._sut = sut if sut is not None else SystemUnderTest("Unknown SUT")
        assert isinstance(self._sut, SystemUnderTest)
        assert isinstance(self._cases, list)

    def __str__(self):
        s = "\n".join(("configuration: {}". format(self.name),
                       "  setup={}".format(str(self.setup)),
                       "  cleanup={}".format(str(self.cleanup)),
                       "  cases={}".format([str(s) for s in self.testcases]),
                       "  SUT:\n'{}'".format(str(self._sut))
                       ))
        return s

    @property
    def sut(self):
        return self._sut

    @property
    def systemUnderTest(self):
        return self._sut

    @property
    def testcases(self):
        return self._cases

    def addTestCase(self, case):
        assert isinstance(case, TestCase)
        self._cases.append(case)

    def toJson(self):
        """ """
        return json.dumps(self, cls=_ConfigJsonEncoder, indent=4)

    def toText(self):
        """ """
        pass

    def toXml(self):
        """ """
        a = """<Configuration name="{}">\n""".format(self.name, )
        sut = "{}\n".format(self.sut.toXml())
        s = "<Setup>\n{}</Setup>\n".format(self.setup.toXml())
        c = "<Cleanup>\n{}</Cleanup>\n".format(self.cleanup.toXml())
        # a little functional magic: we run 'toXml()' method on every step and
        # join the steps' XML strings using 'reduce()'
        l = reduce(self.__join, 
                [case.toXml() for case in self.testcases])
        return "".join((a, sut, s, c, l, "</Configuration>\n"))

    def __join(self, s1, s2):
        return "\n".join((s1, s2))

    def toHtml(self, short=True, cssClass=None):
        """Returns the HTML representation of the class instance.
        The 'short' parameter defines the form of the HTML: if true, longer and
        prettier HTML is returned; otherwise shorter, table-oriented HTML is
        returned. The 'cssClass' parameter optional CCS class name for '<div>'
        element.
        """
        sStatus = TestResult(self.setup.returncode) # setup status
        cStatus = TestResult(self.cleanup.returncode) # cleanup status
        if short:
            return self._shortHtml(cssClass, sStatus, cStatus)
        return self._longHtml(cssClass, sStatus, cStatus)

    def _shortHtml(self, cssClass, sStatus, cStatus):
        """Returns the shorter, table-oriented HTML of the class instance."""
        if cssClass:
            d = """<div id="configuration" class="{}">""".format(cssClass)
        else:
            d = """<div id="configuration" >"""
        h = "<h2>Configuration: {}</h2>".format(self.name)
        sut = self.sut.toHtml()
        s = "<p><table><tr><td>Setup</td><td>{}</td><td>{}</td></tr>".format(
                self.setup.toHtml(), str(sStatus))
        c ="<tr><td>Cleanup</td><td>{}</td><td>{}</td></tr></table></p>".format(
                self.cleanup.toHtml(), str(cStatus))
        cases = reduce(self.__join, [tc.toHtml(True) for tc in self.testcases])
        return "\n".join((d, h, sut, s, c, cases, "</div>"))

    def _longHtml(self, cssClass, sStatus, cStatus):    
        """Returns the longer and prettier HTML of the class instance."""
        if cssClass:
            d = """<div id="configuration" class="{}">""".format(cssClass)
        else:
            d = """<div id="configuration" >"""
        h = "<h2>Configuration: {}</h2>".format(self.name) # header
        sut = self.sut.toHtml() # SUT part
        s = "<p><b>Setup:</b> {}</p>".format(self.setup.toHtml(short=False))
        c = "<p><b>Cleanup:</b> {}</p>".format(self.cleanup.toHtml(short=False))
#        s = self.__create("Setup") # setup part
#        c = self.__create("Cleanup") # cleanup part
        cases = reduce(self.__join, [tc.toHtml(False) for tc in self.testcases])
        return "\n".join((d, h, sut, s, c, cases, "</div>"))

    def __create(self, action):
        return "<p>{}: {}</p>".format(action, self.setup.toHtml(short=False))

    def execute(self, **kwargs):
        """Overriden method from Runnable mixin."""
        # define indentation level for printouts
        indent_lvl = 2
        # string builder 
        text = StringIO.StringIO()
        # write system-under-test information into output
        text.write("{}\n".format(str(self.sut)))
        # execute setup actions    
        failed = self._executeSetup(text, indent_lvl, **kwargs)
        # execute cases
        for case in self.testcases:
            if not failed: 
                text.write("\n    >>> Executing test case: '{}'\n".format(
                                                                    case.name))
                status, output = case.execute(**kwargs)
            else:
                output = "\n    >>> Test case '{}' SKIPPED)\n".format(case.name)
                case.status.result = TestStatus.NOT_TESTED
            text.write("    ### STATUS='{}'\n".format(str(status)))
            text.write("    ### OUTPUT ###\n{}\n    ### END ###\n".format(
                                                                       output))
        # execute cleanup actions (only if setup did not fail)  
        if not failed:
            self._executeCleanup(text, indent_lvl, failed, **kwargs)
        return text.getvalue()

class _ConfigJsonEncoder(json.JSONEncoder):
    """Custom JSON encoder for Configuration class"""

    def default(self, obj):
        if isinstance(obj, Configuration):
            d = dict()
            d["name"] = obj.name
            d["sut"] = obj.sut.toJson()
            d["setup"] = obj.setup.toJson()
            d["cleanup"] = obj.cleanup.toJson()
            d["cases"] = [i.toJson() for i in obj.testcases]
            return d
        return json.JSONEncoder.default(self, obj)

class ConfigJsonDecoder(json.JSONDecoder):
    """Custom JSON decoder for Configuration class"""

    def decode(self, jsontext):
        # convert the JSON text into Python dictionary
        cfgDict = json.loads(jsontext)
        # define default values
        name = "Untitled Configuration"
        setup = []
        cleanup = []
        suts = []
        cases = None
        #
        if "name" in cfgDict:
            name = cfgDict["name"]
        if "cases" in cfgDict:
            cases = []
            for case in cfgDict["cases"]:
                cases.append(TestCaseJsonDecoder().decode(case))
        if "setup" in cfgDict:
            setup = ActionJsonDecoder().decode(cfgDict["setup"])
        if "cleanup" in cfgDict:
            cleanup = ActionJsonDecoder().decode(cfgDict["cleanup"])
        if "sut" in cfgDict:
            sut = SutJsonDecoder().decode(cfgDict["sut"])
        assert cases is not None, "Configuration needs test cases..."
        return Configuration(name, setup, cleanup, sut, cases)
        
# TESTING ####################################################################

def runtests():
    print( "Starting unit tests...")
    # SUT
    _sut = SystemUnderTest("SUT-name", suttype=1, ip="129.234.23.233",
            version="1.0", description="A short description")
    cfg = Configuration("a config", sut=_sut)
    # add some setup and cleanup actions
    a1 = ScriptedAction("test/scripts/test.rb", "arg1")
    a2 = ScriptedAction("test/scripts/hello.jar", "arg1 arg2")
    cfg.setup = a1
    cfg.cleanup = a2
    # add some test steps
    s1 = TestStep("the first step")
    s1.action = a1
    s2 = TestStep("the second step")
    s2.action = a2
    s3 = TestStep("the third step")
    s3.action = a1
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
    cfg.addTestCase(c1)
    cfg.addTestCase(c2)
    cfg.addTestCase(c3)
    print(str(cfg))
    print()
    j = cfg.toJson()
    print(j)
    c = ConfigJsonDecoder().decode(j)
    print("type: {}\ndata='{}'".format(type(c), str(c)))
    print(">>> executing config....")
    out = c.execute()
    print("XML={}".format(c.toXml()))
    print("HTML={}".format(c.toHtml(True)))
    print("HTML={}".format(c.toHtml(False)))
#    print(out)

if __name__ == '__main__':
    from teststep import TestStep
    print(__doc__)
    runtests()
