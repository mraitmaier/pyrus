"""
   testable.py - 

   NOTE: this module should not be run as a standalone scripts, excepts for
   built-in tests.

"""
# HISTORY ####################################################################
#                       
# 0.0.1     Mar11   MR # Initial version
#                       
##############################################################################
__description__ = "a _Testable abstract class definition"
__version__ = "0.1"
_author__ = "Miran R."

from action import _Action, NoOpAction

class _Testable(object):
    """
        _Testable - an abstract class for all testable items
    """

    def __init__(self, name, setup, cleanup):
        self._name = name
        self._setup = setup if setup is not None else NoOpAction()
#        self._setup = setup 
        self._cleanup = cleanup if setup is not None else NoOpAction()
#        self._cleanup = cleanup 
        # let's check the setup/cleanup instance
        assert isinstance(self._setup, _Action)
        assert isinstance(self._cleanup, _Action)

    @property
    def name(self):
        return self._name

    @property
    def setup(self):
        return self._setup

    @setup.setter
    def setup(self, val):
        assert isinstance(val, _Action)
        self._setup = val

    @property
    def cleanup(self):
        return self._cleanup

    @cleanup.setter
    def cleanup(self, val):
        assert isinstance(val, _Action)
        self._cleanup = val

#    def addSetupAction(self, action):
#        """ """
#        assert isinstance(action, _Action)
#        self._setup.append(action)
#        print("DEBUG: adding setup action for '{}'".format(self.name))

#    def addCleanupAction(self, action):
#        """ """
#        assert isinstance(action, _Action)
#        self._cleanup.append(action)
#        print("DEBUG: adding cleanup action for '{}'".format(self.name))

    def toJson(self):
        raise NotImplementedError
