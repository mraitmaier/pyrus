"""
      executable.py - base classes for all executable code

      NOTE: this script is not to be used standalone, execept for testing
      purposes!  
"""
# HISTORY ####################################################################
#
#   0.1.0   MR  Mar11   Initial version (moderately tested)
##############################################################################
__description__ = "an Executable class implementation"
__version__ = "0.1.0"
__author__ = "Miran R."

import os
from subprocess import Popen, PIPE, STDOUT

class Executable(object):
    """
        Executable - abstract class implementing the executable script
    """
    def __init__(self, command):
        assert command is not None
        assert command != ""
        self.__cmd = command    # a script to be executed
        self._env = os.environ  # dict for environment vars

    def __str__(self):
        return "{}".format(self.command)

    @property       
    def command(self):
        """Returns the script name """
        return self.__cmd

    def setEnv(self, key, val):
        self._env[key] = val

    def getEnv(self, key):
        return self._env[key]

    @property
    def environ(self):
        return self._env

    def _checkScript(self):
        """Checks for existence of the script"""
        if not os.path.exists(self.__cmd):
            return False
        return True

    def _ExeError(self, exe, error):
        """Saves an 'executable missing' error message as output text"""
        return "Executable '{}' not found on system.\n{}".format(exe, error)

    def _ScriptError(self):
        """Saves an 'script missing' error message as output text"""
        return "Script '{}' does not exist".format(self.command)

    def execute(self, executable, args="", shell=False):
        """Executes the script/executable"""
        assert args is not None
        assert executable is not None
        rc = 1
        output = ""
        # check if executable even exists; if so, execute it; otherwise fail
        if self._checkScript():
            cmdlist = []
            # we need to create a proper list of arguments for Popen to run   
            if isinstance(executable, list):
                cmdlist = executable[:] # copy list
                cmdlist.append(self.command)
            else:
                cmdlist = [executable, self.command]
            # extend the list, if command-line arguments are present
            if args != "":
                cmdlist.extend(args.split())
            # now execute it and get RC and output text
            try:
                proc = Popen(cmdlist, env=self.environ, shell=shell, 
                             stdin=PIPE, stdout=PIPE, stderr=STDOUT)
                (output, errors) = proc.communicate() 
                rc = proc.returncode
            except OSError as oserror: 
                output = self._ExeError(executable, oserror)
        else:
            output = self._ScriptError()
        return (rc, output) 

###################################################################
if __name__ == '__main__':
    print(__doc__)
