"""
   priority.py - 

   NOTE: this module should not be run as a standalone scripts, excepts for
   built-in tests.

"""
# HISTORY ####################################################################
#                       
#  1 Mar11   MR # initial version
#  2 Jan12   MR # Priority class reimplemented using enums
#  3 Jan12   MR # Ported to Py3
#                       
##############################################################################
__description__ = "a priority class definition"
__version__ = "3"
_author__ = "Miran R."

from pyrus.core.enum import enum

Priority = enum(("ERROR", "LOW", "MEDIUM", "HIGH"))

def toPriority(strval):
    """ """
    strval = strval.upper()
    if strval in ["LOW", "L"]:
        return Priority.LOW
    elif strval in ["MEDIUM", "MED", "M"]:
        return Priority.MEDIUM
    elif strval in ["HIGH", "H"]:
        return Priority.HIGH
    else:
        return Priority.ERROR
