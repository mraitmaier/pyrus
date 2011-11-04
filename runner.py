"""
   runer.py - 

   NOTE: this module should not be run as a standalone scripts, excepts for
   built-in tests.
"""
# HISTORY ####################################################################
#
#   0.0.1   Jun11   MR  Initial version of the file
##############################################################################
from __future__ import print_function

__description__ = "Pyrus test runner application"
__version__ = "0.0.1"
__author__ = "Miran R."

import sys
import os
import json
import argparse
import logging, logging.handlers
from datetime import datetime
#from time import sleep
from pyrus.core.collector import Collector
from pyrus.core.testset import TestSetJsonDecoder
from pyrus.core.testrun import TestRun
from pyrus.utils.iputils import check_ip
from pyrus.core.testresult import TestStatus, TestResult
from pyrus.core.error import Error
from pyrus.core.reporter import ReporterFactory, HtmlReporter, XmlReporter

# try to determine PYRUSROOT value; if not, define the default value
#try:
#    PYRUSROOT = os.environ["PYRUSROOT"]
#except KeyError:
#    PYRUSROOT = "."
#PYRUS_CFG_DIR = os.path.join(PYRUSROOT, "cfg")

# Where to store results? Normally this is "$HOME/results".
# Windows is of course an exception, we use %USERPROFILE% value as a base.    
if sys.platform == "win32":
    PYRUS_RESULTS_DIR = os.path.join(os.environ["USERPROFILE"], "results")
else:
    PYRUS_RESULTS_DIR = os.path.expanduser(os.path.join("~", "results"))

# utility strings are defined
START_OUTPUT_STR = "### OUTPUT #{}".format("#"*24)
END_OUTPUT_STR =   "### OUTPUT END #{}".format("#"*20)

def now():
    """Generates formatted current timestamp: "YYYY/MM/DD HH:MM:SS""" 
    return "%s" % datetime.now().strftime("%Y/%m/%d %H:%M:%S")

def fileStamp():
    """Generates the formatted current timestamp for use in filenames"""
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

def _createDefLogName(tsname):
    """ """
    return "_".join((tsname, fileStamp()))

class Runner(object):
    """
        Runner - a class that executes the test run

    Well, it actually executes the test set, the TestRun class is just a
    container for TestSet, adding more information about the test run.

    Input params:
        input   - configuration file that defines the set of tests to be 
                  executed. Currently, XML and JSON formats are accepted as an
                  input configuration format. The 'collector' module can
                  dynamically determine what kind of file is supplied and can
                  parse both formats.
        logfile - custom name for the log where all messages are being logged
                  (a default filename is generated if empty)
        syslog  - IP address of the syslog server, if needed (if empty, sending 
                  to syslog server is omitted)
        workdir - custom working directory where logs and other files will be
                  stored. If empty, "$HOME/results" is defined by default.
                  This is also true for Windows platform where %USERPROFILE% is
                  used as a base.
        debug   - enable debug mode (only for testing and debugging purposes)  
    """
    def __init__(self, input, workdir, logfile=None, syslog=None, cssfile=None,
                                       xsltfile=None, debug=False):
        assert input is not None
        self._testrun = None
        self._log = None
        self._debug = debug
        self._css = cssfile
        self._xslt = xsltfile
        self._init(input, workdir, logfile, syslog) # initialize data structs

    @property
    def log(self):
        return self._log 

    def __str__(self):
        s = "\n".join(("The Runner Object instance:",
                       "\ttest set: {}".format(self._testrun.testset.name),
                       "\tworking dir: {}".format(self._workdir),
                       "\tlogfile: {}".format(str(self._log)),
                       "\tCSS file: {}". format(str(self._css)),
                       "\tXSLT file: {}".format(str(self._xslt)),
                       "\tdebug: {}".format(self._debug),
                       ))
        return s

    def _init(self, input, workdir, logfile, syslog):
        """Initialize the data structures"""
        # if configuration file is specified, parse it; otherwise exit    
        if input:
            try:
                col = Collector(input)
            except Error as ex:
                print(ex)
                print("Exiting...")
                raise SystemExit(1)
            self._testrun = TestRun(col.testset)
        else:
            print("Input configuration file not defined. Exiting...")
            raise SystemExit(1)
        # create default working dir if needed; create it if it does not exist
        if workdir:
            self._workdir = workdir
        else:
            self._workdir = os.path.join(PYRUS_RESULTS_DIR, "_".join((
                self._testrun.testset.name.replace(" ", "_"), fileStamp())))
        if not os.path.exists(self._workdir):
            os.makedirs(self._workdir)
        # define path to logfile and create logfile itself
        if logfile is not None:
            logfile = os.path.join(self._workdir, logfile)
        else:
            logfile = ".".join((os.path.join(self._workdir, "output"), "log"))
        self._createLogger(logfile, syslog)

    def _createLogger(self, filename, syslog=None):
        """Creates the logger and the appropriate handlers."""
        self._log = logging.getLogger("Runner")
        self._log.setLevel(logging.INFO)
        timeForm = "%Y-%m-%d %H:%M:%S"
        f1 = logging.Formatter("%(asctime)s - %(name)s - %(message)s", timeForm)
        f2 = logging.Formatter(
               "%(asctime)s - %(name)s - %(levelname)s - %(message)s", timeForm)
        # default handler is sys.stdout
        sHandler = logging.StreamHandler(sys.stdout)
        sHandler.setLevel(logging.WARNING)
        sHandler.setFormatter(f1)
        self._log.addHandler(sHandler)
        # we specify logging to file
        fHandler = logging.FileHandler(filename, mode="a", encoding="utf-8")
        fHandler.setFormatter(f2)
        self._log.addHandler(fHandler)
        self.log.warning("Logger created successfully")
        self.log.warning("Everything will be logged to '{}'".format(filename))
        # syslog logger is added if syslog IP address is specified
        if syslog is not None and check_ip(syslog):
            nHandler = logging.handlers.SysLogHandler((syslog, 514))
            nHandler.setFormatter(f2)
            self._log.addHandler(nHandler)
            self.log.warning("Syslog logger created: '{}".format(syslog))
        else:
            self.log.warning( "Syslog logger will NOT be created.")
        if self._debug:
            self._log.setLevel(logging.DEBUG)
            self.log.warning("Debug mode enabled.")

    def _runSetup(self, setup, **kwargs):
        """Run the setup script and check the success."""
        assert setup is not None
        failed = False
        setup.execute(**kwargs)
        if setup.returncode == TestStatus.FAIL:
            failed = True
        return failed

    def _cleanupCase(self, case):
        """Clean up statuses for steps and cleanup action when setup fails."""
        assert case is not None
        for step in case.steps:
            step.status.result = TestStatus.NOT_TESTED
        case.cleanup.status = TestStatus.NOT_TESTED
        
    def _runTestCase(self, tc, **kwargs):
        """Execute a single test case"""
        self.log.warning("Starting test case: '{}'". format(tc.name))
        # execute setup script
        self.log.warning("Executing setup action")
        failed = self._runSetup(tc.setup, **kwargs)
        if failed:
            self.log.error(
                    "Setup action failed. There's no point to continue...")
            tc.status.result = TestStatus.FAIL
            self._cleanupCase(tc)
            return 
        else:
            self.log.warning("Setup action exited with RC='{}'".format(
                        tc.setup.returncode))
            self.log.info(START_OUTPUT_STR)
            self.log.info(tc.setup.output)
            self.log.info(END_OUTPUT_STR)
        # execute a case
        status, output = tc.execute(**kwargs)
        self.log.warning("Test case status: {}".format(str(status)))
        self.log.info(START_OUTPUT_STR)
        self.log.info(output)
        self.log.info(END_OUTPUT_STR)
        # execute cleanup script
        self.log.warning("Executing cleanup action")
        tc.cleanup.execute(**kwargs)
        self.log.warning("Cleanup action exited with RC='{}'".format(
                        tc.cleanup.returncode))
        self.log.info(START_OUTPUT_STR)
        self.log.info(tc.cleanup.output)
        self.log.info(END_OUTPUT_STR)
        # finish
        self.log.warning("Test Case '{}' finished.".format(tc.name))
        return True

    def _runConfig(self, cfg, **kwargs):
        """Execute a single configuration."""
        self.log.warning("Starting configuration: '{}'".format(cfg.name))
        self.log.info(str(cfg.systemUnderTest))
        # execute setup script
        self.log.warning("Executing setup action")
        failed = self._runSetup(cfg.setup, **kwargs)
        if failed:
            self.log.error(
                    "Setup action failed.There's no point to continue... ")
            return 
        else:
            self.log.warning("Setup action exited with RC='{}'".format(
                        cfg.setup.returncode))
            self.log.info(START_OUTPUT_STR)
            self.log.info(cfg.setup.output)
            self.log.info(END_OUTPUT_STR)
        # execute test cases
        for tc in cfg.testcases:
            self._runTestCase(tc, **kwargs)
        # execute cleanup script
        self.log.warning("Executing cleanup action")
        cfg.cleanup.execute(**kwargs)
        self.log.warning("Cleanup action exited with RC='{}'".format(
                        cfg.cleanup.returncode))
        self.log.info(START_OUTPUT_STR)
        self.log.info(cfg.cleanup.output)
        self.log.info(END_OUTPUT_STR)
        # finish
        self.log.warning("Configuration '{}' finished.".format(cfg.name))

    def run(self, **kwargs):
        """Run the tests."""
        ts = self._testrun.testset # we need a test set to be run
        start = now()
        self._testrun.started = start
        self.log.warning("Starting Test Set: '{}'".format(ts.name))
        self.log.warning("Execution started at '{}'".format(start))
        # execute setup 
        self.log.warning("Executing setup action")
        failed = self._runSetup(ts.setup, **kwargs)
        # if setup script fails, exit immediatelly
        if failed:
            self.log.error("Setup action failed.")
            self.log.error("There's no point to continue. Exiting...")
            self.__finish()
            return
        else:
            self.log.warning("Setup action exited with RC='{}'".format(
                        ts.setup.returncode))
            self.log.info(START_OUTPUT_STR)
            self.log.info(ts.setup.output)
            self.log.info(END_OUTPUT_STR)
        # exexute configurations
        for cfg in ts.configs:
            self._runConfig(cfg, **kwargs)
        # execute cleanup 
        self.log.warning("Executing cleanup action")
        ts.cleanup.execute(**kwargs)
        self.log.warning("Cleanup action exited with RC='{}'".format(
                        ts.cleanup.returncode))
        self.log.info(START_OUTPUT_STR)
        self.log.info(ts.cleanup.output)
        self.log.info(END_OUTPUT_STR)
        # finish
        self.__finish()

    def __finish(self):
        """Aux method that finishes the test set execution."""
        stop = now()
        self.log.warning("Test Set '{}' finished.".format(
                    self._testrun.testset.name))
        self.log.warning("Execution finished at {}.".format(stop))
        self._testrun.finished = stop

    def createReport(self, name=None, include=None):   
        """Create and write a test run report.  
        If name is empty (None), methot creates the default report name. In
        this case, report is fixed to HTML.
        Otherwise, method tries to automagically determine the file type and to
        create an appropriate reporter class instance. 
        Currently only XML and HTML reports are supported.
        """
        # if name is empty, create default (type is HTML)
        if not name:
            name = "report.html" # HTML report by default
        fullname = os.path.join(self._workdir, name)
        self.log.warning("Trying to create report: '{}'".format(fullname))
        # now create it 
        rep = None
        try:       
            rep = ReporterFactory(fullname)
        except Error as ex:
            self.log.error("Cannot write report file '{}'".format(fullname))
            self.log.error(ex)
            return
        # check for file to include (CSS or XSLT); local include has precedence
        if not include:    
            if isinstance(rep, HtmlReporter):
                include = self._css
            elif isinstance(rep, XmlReporter):
                include = self._xslt
        # and write it
        try:
            rep.write(self._testrun, include)
            self.log.warning("Report created.")
        except (Error, IOError) as ex:
            self.log.warning("Report NOT created.")
            self.log.error(ex)

def parseArgs():
    """Parse command-line arguments"""
    p = argparse.ArgumentParser()    
    p.add_argument("-i", metavar="FILE", dest="input", 
            help="Name of the input (JSON) file")
    p.add_argument("-l", metavar="LOGFILE", dest="logfile", default=None, 
            help="Name of the logfile")
    p.add_argument("-s", metavar="SYSLOG-IP-ADDR", dest="syslog", default=None,
            help="IP address of the syslog file")
    p.add_argument("-d", dest="debug", action="store_true", default=False,
            help="enable debug mode (for testing purposes only)")
    p.add_argument("-w", metavar="WORKDIR", dest="workdir", 
            default=None,
            help="Specify working directory (default is '$HOME/results')")
    p.add_argument("-r", metavar="REPORTNAME", dest="report", default=None,
            help="set custom report name (default is ....)")
    p.add_argument("-c", metavar="CSS-FILE", dest="cssfile", default=None,
            help="a path to CSS file that will included in HTML report")
    p.add_argument("-x", metavar="XSLT-FILE", dest="xsltfile", default=None,
            help="a XSLT file that will included into XML report""")
    return p.parse_args()

if __name__ == '__main__':
    args = parseArgs()
    r = Runner(args.input, args.workdir, args.logfile, args.syslog, 
            args.cssfile, args.xsltfile, args.debug)
    r.run()
    r.createReport(args.report)
