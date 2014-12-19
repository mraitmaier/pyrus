"""
   testable.py - 

   NOTE: this module should not be run as a standalone scripts, excepts for
   built-in tests.

"""
# HISTORY ####################################################################
#                       
#   1   Mar11   MR  Initial version
#   2   Dec14   MR  Ported to Py3
#                       
##############################################################################
__description__ = "a _Testable abstract class definition"
__version__ = "2"
_author__ = "Miran R."

from pyrus.core.action import _Action, NoOpAction

class _Testable(object):
    """
        _Testable - an abstract class for all testable items
    """

    def __init__(self, name, setup, cleanup):
        self._name = name
        self._setup = setup if setup is not None else NoOpAction()
        self._cleanup = cleanup if setup is not None else NoOpAction()
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

    def toJson(self):
        raise NotImplementedError
