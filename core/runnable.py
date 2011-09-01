"""
   runnable.py - 

   NOTE: this module should not be run as a standalone scripts, excepts for
   built-in tests.

"""
# HISTORY ####################################################################
#                       
# 0.0.1     Apr11   MR # Initial version
#                       
##############################################################################
__description__ = "a _Runnable mixin implementation"
__version__ = "0.0.1"
__author__ = "Miran R."

import logging
from testresult import TestResult, TestStatus

class Runnable(object):
    """Abstract base class for all containers"""

    def __init__(self, logger=None):
        """ """
        if logger:
            self._logger = logger
        else:
            self.logger = logging.getLogger("Runnable")
            self.logger.addHandler(logging.NullHandler())
        self.logger.warning("Logger {} created.".format(self.logger.getName()))
    
    @property
    def logger(self):
        return self._logger

    def execute(self, **kwargs):
        """ """
        raise NotImplementedError

    def _executeSetup(self, text, indent_lvl, **kwargs):
        """Executes the setup action list. 
        It can be used for all _Containers."""
        assert text is not None
        failed = False
        # indent string: string are right-aligned, space-padded, depend on
        # indent level
        indented = "{:>}".format(" "*(2*indent_lvl))
        # execute setup action
        #print(">>> Executing setup action: '{}'\n".format(str(a)))
        text.write("\n{}>>> Executing setup action: '{}'\n".format(
                                                indented, str(self.setup)))
        self.setup.execute(**kwargs)
        text.write("{}### RC='{}'\n".format(indented, self.setup.returncode))
        text.write("{0}### OUTPUT ###\n{1}\n{0}### END ###\n".format(
                                                indented, self.setup.output))
        # if any setup action fails, interrupt execution of the
        # configuration, there's no point to continue
        if self.setup.returncode == TestStatus.FAIL:
            text.write("{}ERROR: The '{}' setup action failed.\n".format(
                                                indented, str(self.setup)))
            text.write("{}The '{}' execution STOPPED.\n".format(
                                                          indented, self.name))
            failed = True
        return failed

    def _executeCleanup(self, text, indent_lvl, failed, **kwargs):
        """Executes the cleanup action list.
        It can be used for all _Containers."""
        assert text is not None
        assert failed in [True, False]
        # create an indentation string for messages
        indented = "{:>}".format(" "*(2*indent_lvl))
        # execute cleanup actions
        if not failed:
            text.write("\n{}>>> Executing cleanup action: '{}'\n".format(
                                                  indented, str(self.cleanup)))
            self.cleanup.execute(**kwargs)
            text.write("{}### RC='{}'\n".format(indented, 
                                                      self.cleanup.returncode))
            text.write("{0}### OUTPUT ###\n{1}\n{0}### END ###\n".format(
                                    indented, self.cleanup.output))
        else:
            text.write("{}>>> cleanup action: '{}' SKIPPED\n".format(
                                             indented, str(self.cleanup)))

