"""
    dos2unix.py - small python script implementing the wrapper for 'dos2unix'
                  utility. Could be quite handy sometimes...

    NOTE: this script shouldn't be run standalone (except for testing purposes),
    it should be used as python module.

    Example usage:

        from atf.utils.dos2unix import dos2unix
        
        f = "somefile.txt"
        status = dos2unix(f)
        print status

"""    
__description__ =  "dos to unix text conversion"
__version__ = "1.0.0"
__author__ = "Miran R."

import os, sys

# check platform
pfrom = sys.platform
if pform in ["linux2", "cygwin"]:
    EXE = "dos2unix"
elif pform in ["win32"]:
    EXE = "dos2unix.exe"
else:
    raise ValueError("dos2unix: wrong platform {}".format(pform))

def dos2unix(textfile):
    """Converts DOS-style (ctrl-r,ctrl-n) line ending in text file to
    unix-style line ending(ctrl-n)"""
    # check for existence
    if not os.path.exists(textfile):
        print "File '%s' does not exist. Exiting..." % textfile
        return False
    # create a command to be executed and run it
    cmd = "%s %s" % (EXE, textfile)
    rc = os.system(cmd)
    # if return code is 0, all is OK
    if rc == 0:
        return True
    return False
    
def test():
    print "Testing dos2unix utility..."
    f = "test/log.txt"
    status = dos2unix(f)
    print "status: %s" % status 
    print "Stop."

if __name__ == "__main__":
    print __doc__
    test()
