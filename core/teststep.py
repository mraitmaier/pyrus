"""
   teststep.py - 

   NOTE: this module should not be run as a standalone scripts, excepts for
   built-in tests.

"""
# HISTORY ####################################################################
#                       
#  1 Mar11   MR # Initial version
#  2 Dec14   MR # Ported to Py3
#                       
##############################################################################
__description__ = "TestStep class implementation"
__version__ = "2"
__author__ = "Miran R."

import json
from pyrus.core.action import AutomatedAction, NoOpAction, ManualAction, ActionJsonDecoder
from pyrus.core.teststatus import TestStatus, toTestStatus
from pyrus.core.error import Error

class TestStep(object):
    """
    """

    def __init__(self, name, action=NoOpAction(),
                             expected=TestStatus.PASS,
                             status=TestStatus.NOT_TESTED):
        assert name is not None
        self.action = action
        self._name = name
        self._expected = expected
        self.status = status

    def __str__(self):
        s = "\n".join(("test step: {}". format(self.name),
                       "  expected={}".format(self.expected), 
                       "  status={}".format(self.status),
                       "  action={}".format(str(self.action)) ))
        return s

    @property
    def action(self):
        return self._action

    @action.setter
    def action(self, action):
        assert isinstance(action, (NoOpAction, ManualAction, AutomatedAction))
        self._action = action

    @property
    def name(self):
        return self._name

    @property
    def expected(self):
        return self._expected

    @property
    def status(self):
        return self._status
    
    @status.setter
    def status(self, val):
        self._status = val

    def toJson(self):
        """ """
        return json.dumps(self, cls=_TestStepJsonEncoder, indent=4,
                skipkeys=True)

    def toText(self):
        """ """
        return "{} {} {} {}\n".format(self.name, self.expected, 
                                      self.action.toText(), self.status) 
    def toXml(self):
        """ """
        n = """<TestStep name="{}" expected="{}" status="{}">\n""".format(
                self.name, self.expected, self.status)
        a = self.action.toXml()
        return "".join((n, a, "</TestStep>\n"))    

    def toHtml(self, short=True, cssClass=None):
        """Return a HTML respresentation of the TestStep."""
        if short:
            return self._shortHtml(cssClass)
        else:
            return self._longHtml(cssClass)

    def _shortHtml(self, cls):
        """Returns the short (table row) HTML representation of TestStep."""
        if cls:
            r = """<tr class="{}">""".format(cls)
        else:
            r = "<tr>"
        n = "<td>{}</td>".format(self.name)   
        a = "<td>{}</td>".format(str(self.action))
        e = "<td>{}</td>".format(self.expected)
        s = "<td>{}</td>".format(self.status)
        return "".join((r, n, a, e, s, "</tr>"))

    def _longHtml(self, cls):
        """Returns the longer and prettier HTML representation of TestStep."""
        if cls:
            d = """<div class="{}">""".format(cls)
        else:
            d = "<div>"
        n = "<h4>{}</h4>".format(self.name)
        a = "<b>{}</b><br>".format(str(self.action))
        e = "Expected status: {}<br>".format(self.expected)
        s = "Status: {}<br>".format(self.status)
        o = "<i>Output:</i><br>\n<pre>{}</pre>".format(self.action.output)
        return "\n".join((d, n, a, e, s, o, "</div>"))

    def _evaluate(self):
        """Evaluates the execution of the test step."""
        self.status = TestStatus.FAIL
        # we evaluate the action's return code value
        if self.action.returncode == 0:
            status = TestStatus.PASS 
        else: 
            status = TestStatus.FAIL 
        # now we compare it to expected value
        # test case passes only when: 
        #   1. expected=pass and status=pass
        #   2. expected=expected-fail and status=fail
        if (status == TestStatus.PASS and self.expected == TestStatus.PASS):
                self.status = status
        elif (status == TestStatus.FAIL and self.expected == TestStatus.XFAIL):
                self.status = TestStatus.PASS
        return self.status

    def execute(self, **kwargs):
        """ """
        self.action.execute(**kwargs)
        if self.action.isAutomated():
            return self._evaluate(), self.action.output
        else:
            return TestStatus.NOT_TESTED, ""

class _TestStepJsonEncoder(json.JSONEncoder):
    """Custom JSON encoder for TestStep class"""

    def default(self, obj):
        if isinstance(obj, TestStep):
            d = dict()
            d["name"] = obj.name
            d["expected"] = str(obj.expected)
            d["action"] = obj.action.toJson()
            d["status"] = str(obj.status)
            return d
        return json.JSONEncoder.default(self, obj)

class TestStepJsonDecoder(json.JSONDecoder):

    def decode(self, jsontext):
        stepDict = json.loads(jsontext)
        expected = TestStatus.NOT_TESTED
        name = "Untitled test step"
        if "name" in stepDict:
            name = stepDict["name"]
        if "expected" in stepDict:
            expected = toTestStatus(stepDict["expected"])
        if "action" in stepDict:
            action = ActionJsonDecoder().decode(stepDict["action"])
        if "status" in stepDict:
            status = toTestStatus(stepDict["status"])
        else:
            raise Error("TestStep needs an action...")
        return TestStep(name, action, expected, status) 
        
# TESTING ####################################################################
def runtests():
    print( "Starting unit tests...")
    s = TestStep("a test step")
    print((str(s)))
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>")
    act = AutomatedAction("test/scripts/test.py", "arg1")
    s = TestStep("a different test step", act, TestStatus.XFAIL)
    j = s.toJson()
    print(j)
    ts = TestStepJsonDecoder().decode(j)
    print(("type: {} \ndata='{}'".format(type(ts), ts)))
    print("Executing...")
    res, output = s.execute()
    print((str(s)))
    print(("RC={} Output:\n'{}'".format(str(res), output)))
    print(("XML='{}'".format(s.toXml())))
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>")
    act2 = AutomatedAction("test/scripts/test.py")
    s2 = TestStep("another test step", act2, TestStatus.PASS)
    print("Executing again...")
    rs, out = s2.execute()
    print((str(s2)))
    print(("RC={} Output:\n'{}'".format(str(rs), out)))
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>")
    act = AutomatedAction("test/scripts/tet.py")
    s2 = TestStep("false test step", act, TestStatus.XFAIL)
    print("Executing again...")
    rs, out = s2.execute()
    print((str(s2)))
    print(("RC={} Output:\n'{}'".format(str(rs), out)))
    print(("XML='{}'".format(s2.toXml())))
    print(("HTML='{}'".format(s2.toHtml())))
    print(("HTML='{}'".format(s2.toHtml(False))))
    print(("HTML='{}'".format(s2.toHtml(cssClass=".teststep"))))
    print(("HTML='{}'".format(s2.toHtml(False, cssClass=".teststep"))))
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print("Stop")

if __name__ == '__main__':
   print(__doc__)
   runtests()
