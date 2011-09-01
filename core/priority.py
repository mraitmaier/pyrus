"""
   priority.py - 

   NOTE: this module should not be run as a standalone scripts, excepts for
   built-in tests.

"""
# HISTORY ####################################################################
#                       
# 0.0.1     Mar11   MR # This is just an example hot to write history notes
#                       
##############################################################################
__description__ = "a priority class definition"
__version__ = "0.0.1"
_author__ = "Miran R."


class Priority(object):
    """
        Priority -
    """
    
    ERROR = -1
    LOW = 0
    MEDIUM = 1
    HIGH = 2
    Values = [ERROR, LOW, MEDIUM, HIGH]

    @staticmethod
    def valToStr(val):
        """Static method for converting int value to string"""
        if val == Priority.LOW:
            return "low"
        elif val == Priority.MEDIUM:
            return "medium"
        elif val == Priority.HIGH:
            return "high"
        elif val == Priority.ERROR:
            return "error"
        else:
            return "invalid priority"

    @staticmethod
    def strToVal(strVal):
        """ """
        assert strVal is not None
        strVal = strVal.strip().lower()
        if strVal in ["low", "l"]:
            return Priority.LOW
        elif strVal in ["m", "med", "medium"]:
            return Priority.MEDIUM
        elif strVal in ["h", "high"]:
            return Priority.HIGH
        else:
            return Priority.ERROR
    
