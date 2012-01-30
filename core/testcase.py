"""
   testcase.py - 

   NOTE: this module should not be run as a standalone scripts, excepts for
   built-in tests.

"""
# HISTORY ####################################################################
#                       
# 0.0.1     Mar11   MR # initial version
# 0.0.2     Jan12   MR # simplification: TestResult is deprecated, using
#                        (new) TestStatus instead
#                       
##############################################################################
from __future__ import print_function

__description__ = "TestCase class implementation"
__version__ = "0.0.1"
__author__ = "Miran R."

import json
import StringIO
from testable import _Testable
from runnable import Runnable
from action import AutomatedAction, NoOpAction, ManualAction, ActionJsonDecoder
from teststep import TestStep, TestStepJsonDecoder
from teststatus import TestStatus, toTestStatus

class TestCase(_Testable, Runnable):
    """
        TestCase - a wrapper class representing the single test case

    Implements _Testable and Runnable mixins.
    _Testable implements name, setup and cleanup properties.
    Runnable defines execute() method that must be overriden.
    """

    def __init__(self, name, description="", 
                             expected=TestStatus.PASS, 
                             setup=None, cleanup=None, tsteps=None,
                             status=TestStatus.NOT_TESTED):
        assert name is not None
        super(TestCase, self).__init__(name, setup, cleanup)
        self._steps = tsteps if tsteps is not None else list()
        self._desc = description
        self._expected = expected
        self.status = status

    def __str__(self):
        s = "\n".join(("test case: {}".format(self.name),
                       "  description:\n{}".format(self.description),
                       "  expected={}".format(self.expected), 
                       "  status={}".format(self.status), 
                       "  setup={}".format(str(self.setup)),
                       "  cleanup={}".format(str(self.cleanup)),
                       "  steps={}".format([str(s) for s in self.steps])
                       ))
        return s

    @property
    def description(self):
        return self._desc

    @property
    def expected(self):
        return self._expected

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, val):
        self._status = val

    @property
    def steps(self):
        return self._steps

    def addStep(self, step):
        assert isinstance(step, TestStep)
        self._steps.append(step)

    def toJson(self):
        """ """
        return json.dumps(self, cls=_TestCaseJsonEncoder, indent=4)

    def toText(self):
        """ """
        pass

    def toXml(self):
        """Convert the instance into XML representation."""
        a = """<TestCase name="{}" expected="{}" status="{}">\n""".format(
                self.name, self.expected, self.status)
        d = "<Description>{}</Description>\n".format(self.description)
        s = "<Setup>\n{}</Setup>\n".format(self.setup.toXml())
        c = "<Cleanup>\n{}</Cleanup>\n".format(self.cleanup.toXml())
        # a little functional magic: we run 'toXml()' method on every step and
        # join the steps' XML strings using 'reduce()'
        l = reduce(lambda x,y: "".join((x,y)), 
                   [step.toXml() for step in self.steps])
        return "".join((a, d, s, c, l, "</TestCase>\n"))

    def toHtml(self, short=True, cssClass=None):
        """Convert the instance into HTML representation."""
        sStatus = ""
        cStatus = ""
        if self.setup.isAutomated():
            sStatus = TestStatus.PASS if self.setup.returncode == 0 else \
                TestStatus.FAIL
        if self.cleanup.isAutomated():
            cStatus = TestStatus.PASS if self.cleanup.returncode == 0 else \
                TestStatus.FAIL
        if short:
            return self._shortHtml(cssClass, sStatus, cStatus)
        return self._longHtml(cssClass, sStatus, cStatus)

    def __join(self, s1, s2):
        return "\n".join((s1, s2))

    def _longHtml(self, cssClass, sStatus, cStatus):
        """Return longer and prettier HTML version of the instance."""
        d = """<div class="{}">""".format(cssClass) if cssClass else "<div>"
        h = "<h3>Test Case: {}</h3>".format(self.name)    
        dsc = "<p>{}</p>".format(self.description)
        s = "<p><b>Setup:</b> {}<br>".format(self.setup.toHtml(short=False))
        c = "<b>Cleanup:</b> {}</p>".format(self.cleanup.toHtml(short=False))
        steps = reduce(self.__join, [step.toHtml(False) for step in self.steps])
        return "\n".join((d, h, dsc, s, c, "<p></p>", steps, "</div>"))

    def _shortHtml(self, cssClass, sStatus, cStatus):
        """Return longer and prettier HTML version of the instance."""
        d = """<div class="{}">""".format(cssClass) if cssClass else "<div>"
        h = "<h3>Test Case: {}</h3>".format(self.name)    
        s = "<p><table><tr><td>Setup</td><td>{}</td><td>{}</td></tr>".format(
                self.setup.toHtml(), str(sStatus)) 
        c = "<tr><td>Cleanup</td><td>{}</td><td>{}</td></tr></table></p>".format(
                self.cleanup.toHtml(), str(cStatus)) 
        h1 = "<table><tr><th>Name</th><th>Action</th>"
        h2 = "<th>Expected</th><th>Status</th></tr>"
        steps = reduce(self.__join, [step.toHtml(True) for step in self.steps])
        return "\n".join((d, h, s, c, "<p></p>", h1, h2, steps, 
                    "</table>", "</div>"))

    def _evaluate(self):
        """Self-evaluate the test case status."""
        setup_status = TestStatus.NOT_TESTED # this is temp status for setup
        cases_status = TestStatus.NOT_TESTED # this is temp status for cases
        self.status = TestStatus.NOT_TESTED   
        if self.setup.isAutomated():
            # if setup action fails, the whole case fails
            if self.setup.returncode != 0:
                self.status = TestStatus.FAIL
                return self.status
            else:
                setup_status = TestStatus.PASS
        # evaluate steps
        for s in self.steps:
            # for a case to pass, all steps must pass 
            if s.status != TestStatus.PASS:
                self.status = TestStatus.FAIL
                return self.status
        cases_status = TestStatus.PASS
        # the whole case passes only when...
        if setup_status in [TestStatus.PASS, TestStatus.NOT_TESTED] and \
            cases_status == TestStatus.PASS:
            self.status = TestStatus.PASS
        return self.status

    def execute(self, **kwargs):
        """Overriden method from Runnable mixin."""
        # define indent level for printouts 
        indent_lvl = 3
        # string builder 
        txt = StringIO.StringIO()
        # execute setup actions    
        failed = self._executeSetup(txt, indent_lvl, **kwargs)
        # execute steps
        for step in self.steps:
            if not failed: 
                txt.write("\n      >>> Executing test step: '{}'\n".format(
                                                                    step.name))
                if step.action.isAutomated():
                    step.execute(**kwargs)
            else:
                step.action.output = \
                      "\n      >>> Test Step '{}' Skipped.\n".format(step.name)
                step.status = TestStatus.NOT_TESTED
            txt.write("      ### OUTPUT ###\n{}\n      ### END ###\n".format(
                                                           step.action.output))
        # execute cleanup actions (only if setup section did not fail)   
        if not failed:
            self._executeCleanup(txt, indent_lvl, failed, **kwargs)
        return (self._evaluate(), txt.getvalue())

class _TestCaseJsonEncoder(json.JSONEncoder):
    """Custom JSON encoder for TestCase class"""

    def default(self, obj):
        if isinstance(obj, TestCase):
            d = dict()
            d["name"] = obj.name
            d["description"] = obj.description
            d["expected"] = str(obj.expected)
            d["status"] = str(obj.status)
            d["setup"] = obj.setup.toJson()
            d["cleanup"] = obj.cleanup.toJson()
            d["steps"] = [step.toJson() for step in obj.steps]
            return d
        return json.JSONEncoder.default(self, obj)

class TestCaseJsonDecoder(json.JSONDecoder):
    """Custom JSON decoder for TestCase class"""

    def decode(self, jsontext):
        # JSON text is converted into python dictionary
        tcDict = json.loads(jsontext)
        # default values   
        name = "Untitled test case"
        setup = []
        cleanup = []
        expected = TestStatus.NOT_TESTED
        status = TestStatus.NOT_TESTED
        steps = None
        #    
        if "name" in tcDict:
            name = tcDict["name"]
        if "description" in tcDict:
            desc = tcDict["description"]
        if "expected" in tcDict:
            expected = toTestStatus(tcDict["expected"])
        if "status" in tcDict:
            status = toTestStatus(tcDict["status"])
        if "steps" in tcDict:
            steps = []
            for tc in tcDict["steps"]:
                steps.append(TestStepJsonDecoder().decode(tc))
        if "setup" in tcDict:
            setup = ActionJsonDecoder().decode(tcDict["setup"])
        if "cleanup" in tcDict:
            cleanup = ActionJsonDecoder().decode(tcDict["cleanup"])
        assert steps is not None, "Test case needs some steps..."
        return TestCase(name, desc, expected, setup, cleanup, steps, status)

# TESTING ####################################################################
def runtests():
    print( "Starting unit tests...")
    tc = TestCase("a test case", "A sample description")
    print(str(tc))
    print(tc.toJson())
    print()
    # add some setup and cleanup actions
    a1 = AutomatedAction("test/scripts/test.py", "arg1")
    a2 = AutomatedAction("test/scripts/test.tcl", "arg1 arg2")
    tc.setup = a1
    tc.cleanup = a2
    print(str(tc))
    print()
    # add some test steps
    s1 = TestStep("the first step")
    s1.action = a1
    s2 = TestStep("the second step")
    s2.action = a2
    s3 = TestStep("the third step")
    s3.action = a1
    tc.addStep(s1)
    tc.addStep(s2)
    tc.addStep(s3)
    print(str(tc))
    print()
    j = tc.toJson()
    print(j)
    case = TestCaseJsonDecoder().decode(j)
    print("type : {} \ndata={}".format(type(case), str(case)))
    rc, output = tc.execute()
    print(rc, output)
    print("XML='{}'".format(tc.toXml()))
    print("HTL='{}'".format(tc.toHtml()))
    print("HTL='{}'".format(tc.toHtml(False)))
    print("Stop.")

if __name__ == '__main__':
   print(__doc__)
   runtests()
