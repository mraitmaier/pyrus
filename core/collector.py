"""
   collector.py - 

   NOTE: this module should not be run as a standalone scripts, excepts for
   built-in tests.

"""
# HISTORY ####################################################################
#                       
# 0.0.1     Mar11   MR # This is just an example hot to write history notes
#                       
##############################################################################
__description__ = "an implementation of the Collector class"
__version__ = "0.0.1"
_author__ = "Miran R."

import json 
import os
from error import Error
from testset import TestSet, TestSetJsonDecoder
from action import ActionJsonDecoder
from xml.etree.ElementTree import parse
from action import NoOpAction, ManualAction, AutomatedAction
from teststep import TestStep
from testcase import TestCase
from sut import SystemUnderTest
from teststatus import TestStatus, toTestStatus

JSON_EXT = ".json"
XML_EXT = ".xml"
#TEXT_EXT = [".txt", ".dat"]


class Collector(object):
    """
        Collector -
    """

    def __init__(self, inputfile):
        assert inputfile is not None
        self._ts = None
        self._collect(inputfile)

    @property
    def testset(self):
        return self._ts

    def __str__(self):
        return str(self._ts)

    def _collect(self, filename):
        """A method that chooses the right method to collect data."""
        assert filename is not None
        dontcare, ext = os.path.splitext(filename)
        if ext == JSON_EXT:
            self.__collectJson(filename)
        elif ext == XML_EXT:
            self.__collectXml(filename)
#        elif ext in TEXT_EXT:
#           self.__collectText(filename)
        else:
            raise ValueError("Invalid configuration file: {}".format(filename)) 
           
    def __collectJson(self, filename):
        """Loads a JSON input configuration file and parses it."""
        assert filename is not None
        fin = None
        try:
            fin = open(filename, "r")
        except IOError as ex:
            raise Error(ex)
        s = fin.read()
        fin.close()    
        self._ts = json.loads(s, cls=TestSetJsonDecoder)

    def __collectXml(self, filename):
        """Loads an XML input configuration file and parses it."""
        assert filename is not None
        # let's try to parse XML file   
        try:   
            tree = parse(filename)
        except ParseError as ex:
            raise Error(ex)
        # get root element and check that it has proper tag
        root = tree.getroot() 
        if root.tag != "TestSet":
            raise Error("This is not test set configuration")
        # now we parse root element     
        name = root.get("name")
        testplan = "unknown test plan"
        children = root.getchildren()
        cases = list()
        for child in children:
            if child.tag == "Setup":
                setup = self.__xmlHandleAction(child)
            elif child.tag == "Cleanup":
                cleanup = self.__xmlHandleAction(child)
            elif child.tag == "TestPlan":
                testplan = child.text
            elif child.tag == "TestCase":
                cases.append(self.__xmlHandleCase(child))
            elif child.tag == "SystemUnderTest":
                sut = self.__xmlHandleSut(child)
        self._ts = TestSet(name, testplan, setup, cleanup, cases, sut)

    def __xmlHandleAction(self, elem):
        """ """
        assert elem is not None
        action = NoOpAction()
        txt = elem.text
        xmlscr = elem.find("Script")
        if xmlscr is not None:
            script = xmlscr.text
            xmlargs = elem.find("Args").text
            args = xmlargs if xmlargs is not None else ""
            action = AutomatedAction(script, args)    
#        elif txt != "":
#            action = ManualAction(txt)
        return action

    def __xmlHandleSut(self, elem):
        """ """
        assert elem is not None
        name = elem.get("name")
        xmltype = elem.find("Type")  
        xmlip = elem.find("IP")
        xmlver = elem.find("Version")
        xmldesc = elem.find("Description")
        suttype = xmltype.text if xmltype is not None else ""
        ver = xmlver.text if xmlver is not None else ""
        ip = xmlip.text if xmlip is not None else ""
        desc = xmldesc.text if xmldesc is not None else ""
        return SystemUnderTest(name, suttype, ver, ip, desc) 

    def __xmlHandleCase(self, elem):
        """ """
        assert elem is not None
        name = elem.get("name")
        expected = TestStatus.PASS
        exp = elem.get("expected")
        if exp is not None: 
            expected = toTestStatus(exp) 
        children = elem.getchildren()
        desc = ""
        steps = list()
        for child in children:
            if child.tag == "Description":
                desc = child.text
            elif child.tag == "Setup":
                setup = self.__xmlHandleAction(child)
            elif child.tag == "Cleanup":
                cleanup = self.__xmlHandleAction(child)
            elif child.tag == "TestStep":
                steps.append(self.__xmlHandleStep(child))
        return TestCase(name, desc, expected, setup, cleanup, steps)

    def __xmlHandleStep(self, elem):
        """ """
        assert elem is not None    
        name = elem.get("name")
        expected = toTestStatus(elem.get("expected"))
        action = self.__xmlHandleAction(elem) 
        assert action is not None
        return TestStep(name, action, expected)


#    def __collectText(self, filename):
#        """Loads an XML input configuration file and parses it."""
#        assert filename is not None
#        raise NotImplementedError

# TESTING ####################################################################
FILENAME = "test/testset.json"

def runtests():
    print("Starting unit tests...")
    c = Collector(FILENAME)
    print(str(c))
    print("Stop")

if __name__ == '__main__':
   print(__doc__)
   runtests()
