"""
   container.py - 

   NOTE: this module should not be run as a standalone scripts, excepts for
   built-in tests.

"""
# HISTORY ####################################################################
#                       
# 0.0.1     Apr11   MR # $ Initial version
#                       
##############################################################################
__description__ = "a _Container abstract class implementation"
__version__ = "0.0.1"
__author__ = "Miran R."

import StringIO

class _Container(list):
    """Abstract base class for all containers"""

    def __str__(self):
        s = StringIO.StringIO()
        for i in self:
            s.write("\n  %s" % str(i))
        return s.getvalue()

