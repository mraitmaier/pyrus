"""
   reporter.py - module used for generating XML reports

   NOTE: this module should NOT be used as standalone program, except for
         testing purposes!

   History:
    1.0   - May 2008
            The first stable version
    1.0.1 - July, 10th 2008
            Changed behaviour of the XSL transformation: instead of linking
            the absolute path to XSL file, the XSL file is now copied to the
            results directory; this is more convenient way, I think.
    1.1   - July, 10th 2008
            Added XML schema validation
    1.1.1 - September, 30th 2008
            bugfixes
    2.0   - Jan 2009
            Changes in XML structure reflecting that setups/cleanup are now
            lists; removed the XML schema validation due to lxml dependancy;
    2.0.1 - Mar 2010
            TestObject can be empty.            
    2.1.0 - Feb 2011
            Added HTML report processing
    2.2.0 - Massive refactoring (old XML reporter removed, new XML reporting
            added (new means using 'toXml() methods); the script has been
            substantially reduced...; JsonReporter added;
"""
import os.path 
import sys
import codecs
from datetime import datetime
from shutil import copy
from xml.etree.ElementTree import Element, SubElement, ElementTree
from error import Error

VERSION = "2.2.0"
NAME = "Reporter"
AUTHOR = "Miran R."

DEFAULT_PATH = "."
NEWLINE = "\n"
DEFAULT_START_STR = "Started timestamp unknown"
DEFAULT_FINISH_STR = "Finished timestamp unknown"

# Report types
REPORT_TYPE_UNKNOWN = 0
REPORT_TYPE_XML = 1
REPORT_TYPE_HTML = 2
#REPORT_TYPE_JSON = 3
#REPORT_TYPE_TEXT = 4

def ReporterFactory(name):
    """Factory function that returns the appropriate type of reporter."""
    p, ext = os.path.splitext(name)
    if ext == ".xml":
        return XmlReporter(name)
    elif ext in [".htm", ".html"]:
       return HtmlReporter(name)
    else:
        raise Error("Invalid report file type '{}'".format(ext))

class _Reporter(object):
    """
        _Reporter - abstract class implementing any kind of report generator 
    """

    def __init__(self, path):
        """Ctor"""
        self.__path = path               # path where report to be written

    @property
    def path(self):
        """Returns current XML test report path"""
        return self.__path

    @path.setter
    def path(self, val):
        """Sets a new test report path"""
        assert val is not None or val != ""
        self.__path = os.path.abspath(val)
        (p, f) = os.path.split(val)
        if not os.path.exists(p):
            os.makedirs(p)

    def write(self):
        raise NotImplementedError
  
#class JsonReporter(_Reporter):
#    """
#        JsonReporter - JSON report generator
#    """
#
#    def __init__(self, reportpath):
#        """ Ctor"""
#        assert reportpath is not None
#        super(JsonReporter, self).__init__(reportpath)
#
#    def write(self, obj):
#        """ """
#        assert testset is not None
#        fout = codecs.open(self.Path, "w", "utf8")
#        fout.write(obj.toJson())
#        fout.close()

#class TextReporter(_Reporter):
#    """
#        TextReporter - plain text report generator
#    """
#
#    def __init__(self, reportpath):
#        """Ctor"""
#        assert reportpath is not None
#        super(TextReporter, self).__init__(reportpath)
#
#    def write(self, testset):
#        """ """
#        assert testset is not None
#        fout = codecs.open(self.Path, "w", "utf8")
#        fout.write(testset.toText())
#        fout.close()

class HtmlReporter(_Reporter):
    """ 
        HtmlReporter - HTML report generator
    """
    def __init__(self, reportpath, cssfile=None):
        """Ctor"""
        assert reportpath is not None
        super(HtmlReporter, self).__init__(reportpath)

    def write(self, obj, cssFile=None):
        assert obj is not None
        fout = None
        try:
            fout = codecs.open(self.path, "w", "utf8", "xmlcharrefreplace")
        except IOError as ex:
            raise Error(ex)
        fout.write("<!DOCTYPE HTML>\n")
        fout.write("<html>\n")
        fout.write("<header>\n")
        fout.write("<title>Execution Report for '{}'</title>\n".format(
                    obj.name))
        if cssFile:
            fout.write("""<link rel="stylesheet" type="text/css" """)
            fout.write("""href="%s" />\n""" % cssFile)
        fout.write("</header>\n")
        fout.write("<body>\n")
        fout.write("%s\n" % obj.toHtml())
        fout.write("</body>\n")
        fout.write("</html>\n")
        fout.close()

class XmlReporter(_Reporter):
    """ 
        XmlReporter -
    """

    def __init__(self, reportpath, xsltfile=None):
        """Ctor"""
        super(XmlReporter, self).__init__(reportpath)
        self.__xsltfile = xsltfile # XSL transformation file path
        self._started = False      # flag indicating doc has been started

    def __str__(self):
        s = NEWLINE.join(("XmlReporter class instance:",
                        "  Report path: %s" % self.Path,
                        "  Started Flag: %s" % self.isStarted(),
                        "  TestSet started timestamp:  %s" % self.StartedTag,
                        "  TestSet finished timestamp: %s" % self.FinishedTag,
                        "  XSL Transformation file: %s" % self.XsltFile ))
        return s

    @property
    def xsltFile(self):
        """Returns the name of the XSL Transformation file to be inserted on top
          of XML report."""
        return self.__xsltfile

    @xsltFile.setter
    def xsltFile(self, file):
        """Sets the XSL Transformation file to be inserted on top of the XML
          report"""
        assert file is not None
        self.__xsltfile = os.path.abspath(file)

    def write(self, obj, xsltfile=None):
        """Writes an XML test report file."""
        assert obj is not None
        # if XSLT file name was provided, remember it
        if xsltfile:
            self.xsltFile = xsltfile
        # now open the XML report file to be written
        fout = None
        try:    
            fout = codecs.open(self.path, "w", "utf8", "xmlcharrefreplace")
        except IOError as ex:
            raise Error("Cannot open file '{}'\n\t{}".format(self.path, ex))
        fout.write("""<?xml version="1.0" encoding="utf-8"?>\n""")
        # write XSLT header line, if needed and if it even exists
        if self.xsltFile and os.path.exists(self.xsltFile):
            (head, xsltfile) = os.path.split(self.xsltFile)
            (p, f) = os.path.split(self.path)
            fout.write(
                   """<?xml-stylesheet type="text/xsl" href="{}"?>\n""".format(
                       self.xsltFile))
            # copy the XSL Transform file alongside the XML report
            copy(self.xsltFile, os.path.join(p, xsltfile))
        # write the XML report
        fout.write(obj.toXml())
        fout.close()

############## testing part ##################
TEST_path = "D:/test/testreport.xml" 

def testXml():
    testset = "../cfg/example_ts.xml"
    col = Collector(testset)
    ts = col.testset
    rpt = XmlReporter("d:/test/report.xml")
    rpt.write(ts)
def testHtml():
    testset = "../cfg/example_ts.xml"
    col = Collector(testset)
    ts = col.testset
    #col.display()
    #print ts.toHtml()
    rpt = HtmlReporter("d:/test/htmlreport.html")
    rpt.write(ts)

if __name__ == "__main__":
    print __doc__
    from testset import TestSet
    from collector import Collector
    testXml()
#    testHtml()

