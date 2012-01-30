"""
   priority.py - 

   NOTE: this module should not be run as a standalone scripts, excepts for
   built-in tests.

"""
# HISTORY ####################################################################
#                       
# 0.0.1     Mar11   MR # initial version
# 0.0.2     Jan12   MR # Priority class reimplemented using enums
#                       
##############################################################################
__description__ = "a priority class definition"
__version__ = "0.0.1"
_author__ = "Miran R."

from enum import enum

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
