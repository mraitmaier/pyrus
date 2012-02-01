"""
   action.py - 

   NOTE: this module should not be run as a standalone scripts, excepts for
   built-in tests.

"""
# HISTORY #####################################################################
# 
# 0.0.1     Mar11   MR  Initial version - starting all over again...
# 
###############################################################################
__description__ = "Action clases implementation"
__version__ = "0.0.1"
__author__ = "Miran R."

from teststatus import TestStatus
from exefactory import ExecutableFactory
import StringIO
import json
 
class _Action(object):
    """ 
        _Action - an abstract base class for all action classes 

    Should not be instantiated, use derived classes!
    """

    def isAutomated(self):
        raise NotImplementedError

    def execute(self):
        raise NotImplementedError

    def toHtml(self, **kwargs):
        raise NotImplementedError

    def toXml(self):
        raise NotImplementedError

    def toText(self):
        raise NotImplementedError

    def toJson(self):
        raise NotImplementedError

    def execute(self, args):
        raise NotImplementedError

class NoOpAction(_Action):
    """
        NoOpAction - a do-nothing action
    """

    def __str__(self):
        return "No action"

    def isAutomated(self):
        return False

    def toText(self):
        return ""

    def toXml(self):
        return ""

    def toHtml(self, **kwargs):
        # kwargs are here for compatibility with AutomatedAction and ignored
        return ""

    def toJson(self):
        return json.dumps(self, cls=_ActionJsonEncoder)

class ManualAction(_Action):
    """
        ManualAction - represents a list of manual actions

    This class is to be considered simply as container for manual tests. It's
    just a how-to text to execute the test.
    """
    def __init__(self, description):
        self.description = description

    def __str__(self):
        return "{}".format(self.description)

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, text):
        assert text is not None
        self._description = text

    def isAutomated(self):
        return False

    def toText(self):
        return self.description

    def toJson(self):
        return json.dumps(self, cls=_ActionJsonEncoder, indent=4)

    def toXml(self):
        return "<Description>{}</Description>".format(self.description)

    def toHtml(self, **kwargs):
        # kwargs are for here compatibility with AutomatedAction and ignored
        return self.description

class AutomatedAction(_Action):
    """
        AutomatedAction - represents the single scripted automated action

        The 'script' property represents the actual script to be executed.
        The 'args' property represents the additional arguments that script.
        needs to be executed (CLI arguments).
        The 'status' property is of course the status od the action,
        The ' output' property represents the text caught from STDOUT & STDERR
        when script is run.
    """

    def __init__(self, script, args="", status=-1, output="" ):
        self._script = script    # script to be executed
        self._args = args        # additional arguments for script (if needed)
        self.returncode = status # test return code
        self.output = ""         # output text after script has been run

    def __str__(self):
        return "{0} {1}".format(self.script, self.args) 

    @property
    def script(self):
        """A 'script' property getter"""
        return self._script

    @property
    def args(self):
        """An 'args' property getter"""
        return self._args

    @property
    def returncode(self):
        """The default test status property"""
        return self._rc

    @returncode.setter
    def returncode(self, val):
        """The default test status property setter"""
        assert val is not None, "Test result cannot be empty"
        self._rc = val

    @property
    def output(self):
        """An 'output' property getter."""
        return self._output

    @output.setter
    def output(self, text):
        """An 'output' property setter."""
        self._output = text

    def isAutomated(self):
        """Is this action automated?"""
        return True

    def toText(self):
        """ """
        return str(self)

    def toJson(self):
        return json.dumps(self, cls=_ActionJsonEncoder, indent=4)

    def toXml(self):
        s = "<Script>{}</Script>".format(self.script)
        a = "<Args>{}</Args>".format(self.args)
        r = "<ReturnCode>{}</ReturnCode>".format(self.returncode)
        o = "<Output>{}</Output>".format(self.output)
        return "".join((s, a, "\n", r, "\n", o, "\n"))

    def toHtml(self, **kwargs):
        """Return an HTML representation of the class instance.
        This class defines optional boolean keyword argument called 'short': if
        false, method returs a richer (and longer) version of the HTML with
        status and output; if true (or empty), method returns only simple 
        'script + args' string.
        """
        if "short" in kwargs:
            if not kwargs ["short"]:
                status = self.returncode
                a = "{} <b>{}</b><br>".format(str(self), status) 
                if self.output != "":
                    o = "Output:<br>\n<pre>{}</pre>".format(self.output)
                else:
                    o = "Output: <i>Empty</i><br>"
                return "\n".join((a, o))
        return str(self)

    def execute(self, **kwargs):
        """Execute the action and collect output text and return code"""
        # we produce the right version of executable
        exe = ExecutableFactory(self.script)
        # process environment variables prior to execution, if present
        for key, val in kwargs.items():
            exe.setEnv(key, val) 
        # execute and pick up the results 
        self.returncode, self.output = exe.execute(self.args)

class _ActionJsonEncoder(json.JSONEncoder):
    """Custom JSON encoder for Action classes."""
    def default(self, obj):
        if isinstance(obj, (NoOpAction, AutomatedAction, ManualAction)):
            d = dict()
            if isinstance(obj, NoOpAction):
                return d
            elif isinstance(obj, AutomatedAction):
                d["script"] = obj.script
                if hasattr(obj, "args"):
                    d["args"] = obj.args
            elif isinstance(obj, ManualAction):
                d["description"] = obj.description
            if hasattr(obj, "returncode"):    
                d["rc"] = str(obj.returncode)
            if hasattr(obj, "output"):
                d["output"] = obj.output
            return d
        else:
            return json.JSONEncoder.default(self, obj)

class ActionJsonDecoder(json.JSONDecoder):
    """ """
    def decode(self, jsontext):
        # by default, we have a do-nothing action
        act = NoOpAction()
        d = json.loads(jsontext)
        # if we have a 'script' keyword in JSON, then we're dealing with
        # AutomatedAction
        if "script" in d:
            status = int(d["rc"]) if "rc" in d else -1
            args = d["args"] if "args" in d else ""
            output = d["output"] if "output" in d else ""
            act = AutomatedAction(d["script"], args, status, output)
        # or, if "description" keyword has been found in JSON, 
        # we're dealing with ManualAction
        elif "description" in d:
            status = int(d["rc"]) if "rc" in d else -1
            act = ManualAction(d["description"])
        return act
            
# TESTING #####################################################################
def runtests():
    print("Starting unit tests...")
    print(">>> NoOpAction...")
    a = NoOpAction()
    print(str(a))
    print(a.isAutomated())
    j = a.toJson()
    print("JSON=" + j)
    print("XML={}".format(a.toXml()))
    blah = ActionJsonDecoder().decode(j)
    print("Decoded JSON=" + str(blah))
    print(">>> AutomatedAction...")
    b = AutomatedAction("/this/is/a/script/path", "arg 12 34")
    print(str(b))
    b = AutomatedAction("test/scripts/test.py", "arg 12 34")
    print(str(b))
    print(b.isAutomated())
    j = b.toJson()
    print(j)
    print("executing...")
    #b.execute(env1="something", env2="999")
    b.execute()
    print("RC={}".format(str(b.returncode)))
    print("output='{}'".format(b.output))
    blah = ActionJsonDecoder().decode(j)
    print("Decoded JSON=" + str(blah))
    print("XML={}".format(b.toXml()))
    print("HTML={}".format(b.toHtml()))
    print("HTML={}".format(b.toHtml(short=True)))
    print("HTML={}".format(b.toHtml(short=False)))
    print(">>> ManualAction...")
    c = ManualAction("Manual action 1")
    print str(c)
    j = c.toJson()
    print(j)
    blah = ActionJsonDecoder().decode(j)
    print ("type: {} data: {}".format(type(blah), str(blah)))
    print("XML={}".format(c.toXml()))
    print("HTML={}".format(c.toHtml()))
    print("HTML={}".format(c.toHtml(short=False)))
    print("Stop")

if __name__ == '__main__':
   print __doc__
   runtests()
