"""
   testrun.py - 

   NOTE: this module should not be run as a standalone scripts, excepts for
   built-in tests.

   NOTE: This module is to be regarded as obsolete! TestReport class is the one
   to go.

"""
# HISTORY ####################################################################
#                       
# 0.0.1     Mar11   MR # This is just an example hot to write history notes
# XXXXX     Sep01   MR # This module is now obsolete; TestReport class is the
#                        one to use!!!
#                       
##############################################################################
from __future__ import print_function

__description__ = "a TestRun class implementation"
__version__ = "0.0.1"
_author__ = "Miran R."

from testset import TestSet, TestSetJsonDecoder
import json
from datetime import datetime 

def now():
    """Generates formatted current timestamp: "YYYY/MM/DD HH:MM:SS"""
    return "%s" % datetime.now().strftime("%Y/%m/%d %H:%M:%S")

def fileStamp():
    """Generates the formatted current timestamp for use in filenames"""
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

class TestRun(object):
    """ 
        TestRun -
    """
    def __init__(self, testset, started="", finished=""):
        assert isinstance(testset, TestSet)
        self._ts = testset
        self._start = started
        self._finish = finished

    def __str__(self):
        return "TestRun: test set '{}' executed from {} to {}.".format(
                                self.testset.name, self.started, self.finished)

    @property
    def testset(self):
        return self._ts

    @property
    def started(self):
        return self._start

    @started.setter
    def started(self, val):
        self._start = val

    @property
    def finished(self):
        return self._finish

    @finished.setter
    def finished(self, val):
        self._finish = val

    @property
    def name(self):
        return self.testset.name

    def toJson(self):
        return json.dumps(self, cls=_TestRunJsonEncoder, indent=4)

    def toXml(self):
        s = "<Started>{}</Started>".format(self.started) 
        f = "<Finished>{}</Finished>".format(self.finished)
        ts = self.testset.toXml()
        return "\n".join(("<TestRun>", s, f, ts, "</TestRun>"))

    def toHtml(self, short = True, cssClass=None):
        """Convert the class instance into HTML."""
        h = "<h1>Test run</h1>"
        s = "<p>Started on {}</p>".format(self.started)
        f = "<p>Finished on {}</p>".format(self.finished)
        ts = self.testset.toHtml(short, cssClass)
        return "\n".join((h, s, f, ts))

    def execute(self, **kwargs):
        """Run the testset"""
        self.started = now()   
        output = self._ts.execute(kwargs)
        self.finished = now()   
        return output

class _TestRunJsonEncoder(json.JSONEncoder):
    """Custom JSON encoder for the TestRun class"""

    def default(self, obj):
        if isinstance(obj, TestRun):
            d = dict()
            d["testset"] = obj.testset.toJson()
            d["started"] = obj.started
            d["finished"] = obj.finished
            return d
        return json.JSONEncoder(obj)

class TestRunJsonDecoder(json.JSONDecoder):
    """Custom JSON decoder for the TestRun class"""
    
    def decode(self, jsontext):
        # convert JSON into python dictionary
        runDict = json.loads(jsontext)
        # default values 
        started = ""
        finished = ""
        testset = None
        # decode the dictionary
        if "testset" in runDict:
            testset = TestSetJsonDecoder().decode(runDict["testset"])
        if "started" in runDict:
            started = runDict["started"]
        if "finished" in runDict:
            started = runDict["finished"]
        assert testset is not None, "TestRun needs a TestSet to run..."
        return TestRun(testset, started, finished)

# TESTING ####################################################################

def runtests():
    from collector import Collector
    ts = Collector("../cfg/example.json").testset
    print(">>> Starting tests...")
    n = now()
    print("now="+now())
    print("now="+str(datetime.now()))
    tr = TestRun(ts, n, n)
    print("Started={}".format(tr.started))
    print("Finished={}".format(tr.finished))
    print(str(tr))
    j = tr.toJson()
    print(j)
    bla = TestRunJsonDecoder().decode(j)
    print("typ {}, data='{}'".format( type(bla), str(bla)))
    print("XML={}".format(tr.toXml()))
    print("HTML={}".format(tr.toHtml()))
    print(">>> Stop.")

if __name__ == "__main__":
    print(__doc__)
    runtests()
