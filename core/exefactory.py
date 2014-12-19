"""
   executor.py - implementing wrapper class for executing scripts and programs

"""   
import os
from pyrus.core.pythonscript import PythonScript
from pyrus.core.perlscript import PerlScript
from pyrus.core.tclscript import TclScript
from pyrus.core.ixiatclscript import IxiaTclScript
from pyrus.core.expectscript import ExpectScript
from pyrus.core.nativeexecutable import NativeExecutable
from pyrus.core.javaexecutable import JavaExecutable
from pyrus.core.rubyscript import RubyScript
from pyrus.core.groovyscript import GroovyScript
from pyrus.core.luascript import LuaScript
from pyrus.core.juliaprogram import JuliaProgram

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
_LUA_SCRIPT_EXT = [".lua"]
_JULIA_EXE_EXT = [".jl"]

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
    elif ext in _LUA_SCRIPT_EXT:
        script = LuaScript(cmd)
    elif ext in _JULIA_EXE_EXT:
        script = JuliaProgram(cmd)
    else:
        script = NativeExecutable(cmd)
    return script

def runtests():
    pass
 
if __name__ == "__main__":
   print(__doc__)
   runtests()
