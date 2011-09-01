"""
   executor.py - implementing wrapper class for executing scripts and programs

"""   
import os
from pythonscript import PythonScript
from perlscript import PerlScript
from tclscript import TclScript
from ixiatclscript import IxiaTclScript
from expectscript import ExpectScript
from nativeexecutable import NativeExecutable
from javaexecutable import JavaExecutable
from rubyscript import RubyScript
from groovyscript import GroovyScript

__description__ = "executable factory function implementation"
__version__ = "0.6"
__author__ = "Miran R."

# different script extensions
_PYTHON_SCRIPT_EXT = [".py", ".pyw"]
_PERL_SCRIPT_EXT = [".pl", ".pm"]
_TCL_SCRIPT_EXT = [".tcl"]
_EXPECT_SCRIPT_EXT = [".exp"]
_RUBY_SCRIPT_EXT = [".rb"]
_JAVA_EXE_EXT = [".jar"]
_GROOVY_SCRIPT_EXT = [".groovy"]

def ExecutableFactory(cmd):
    """Tries to resolve what type of the script is to be executed and
    returns the appropriate type of object. If not determined, returns
    None."""
    assert cmd is not None
    # extract the extension for the current script to be executed
    (_dontcare, ext) = os.path.splitext(cmd) 
    script = None
    if ext in _PYTHON_SCRIPT_EXT:
        script = PythonScript(cmd)
    elif ext in _EXPECT_SCRIPT_EXT:
        script = ExpectScript(cmd)
    elif ext in _TCL_SCRIPT_EXT:
        # we have 2 choices here; if script name starts with "ix", this is
        # an IXIA configuration TCL script; otherwise it is a "normal" TCL
        # script
        (dontcare2, scriptname) = os.path.split(cmd)
        if scriptname.startswith("ix"):
            script = IxiaTclScript(cmd)
        else: 
            script = TclScript(cmd)
    elif ext in _PERL_SCRIPT_EXT:
        script = PerlScript(cmd)
    elif ext in _RUBY_SCRIPT_EXT:
        script = RubyScript(cmd)
    elif ext in _JAVA_EXE_EXT:
        script = JavaExecutable(cmd)
    elif ext in _GROOVY_SCRIPT_EXT:
        script = GroovyScript(cmd)
    else:
        script = NativeExecutable(cmd)
    return script

def runtests():
    pass
 
if __name__ == "__main__":
   print __doc__
   runtests()
