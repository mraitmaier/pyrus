"""
   testreport.py - 

   NOTE: this module should not be run as a standalone scripts, excepts for
   built-in tests.

"""
# HISTORY ####################################################################
#                       
#   1   Apr11   MR # Initial version
#   2   Dec14   MR # Ported to Py3
#                       
##############################################################################

__description__ = "a TestReport class implementation"
__version__ = "3"
_author__ = "Miran R."

from pyrus.core.testset import TestSet, TestSetJsonDecoder
import json
from datetime import datetime 

_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

def now():
    """Generates formatted current timestamp: "YYYY/MM/DD HH:MM:SS"""
    return "%s" % datetime.now().strftime(_DATETIME_FORMAT)

class TestReport(object):
    """ 
        TestReport -
    """
    def __init__(self, testset, started, finished):
        assert isinstance(testset, TestSet)
        self._ts = testset
        self._start = started
        self._finish = finished

    def __str__(self):
        return "TestReport: test set '{}' executed from {} to {}.".format(self.testset.name, self.started, self.finished)

    @property
    def testset(self):
        return self._ts

    @property
    def started(self):
        return self._start

    @property
    def finished(self):
        return self._finish

    def toJson(self):
        return json.dumps(self, cls=_TestReportJsonEncoder)

    def toXml(self):
        s = "<Started>{}</Started>".format(self.started)
        f = "<Finished>{}</Finished>".format(self.finished)
        ts = self.testset.toXml()
        return "\n".join(("<TestReport>", s, f, ts, "</TestReport>"))

class _TestReportJsonEncoder(json.JSONEncoder):
    """Custom JSON encoder for the TestReport class"""

    def default(self, obj):
        if isinstance(obj, TestReport):
            d = dict()
            d["testset"] = obj.testset.toJson()
            d["started"] = obj.started
            d["finished"] = obj.finished
            return d
        return json.JSONEncoder(obj)

class TestReportJsonDecoder(json.JSONDecoder):
    """Custom JSON decoder for the TestReport class"""
    
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
            started = datetime.strptime(runDict["started"], _DATETIME_FORMAT)
        if "finished" in runDict:
            finished = datetime.strptime(runDict["finished"], _DATETIME_FORMAT)
        assert testset is not None, "TestReport needs a TestSet to run..."
        return TestReport(testset, started, finished)

# TESTING ####################################################################

def runtests():
    from collector import Collector
    ts = Collector("../cfg/example_ts.xml").testset
    print(">>> Starting tests...")
    print("now="+now())
    print("now="+str(datetime.now()))
    tr = TestReport(ts, now(), now())
    print("Started={}".format(tr.started))
    print("Finished={}".format(tr.finished))
    print(str(tr))
    j = tr.toJson()
    print(j)
    bla = TestReportJsonDecoder().decode(j)
    print("typ {}, data='{}'".format(type(bla), str(bla)))
    print("XML={}".format(tr.toXml()))
    print(">>>>>>>>>")
    print(bla.__dict__)
    print(">>> Stop.")

if __name__ == "__main__":
    print(__doc__)
    runtests()
