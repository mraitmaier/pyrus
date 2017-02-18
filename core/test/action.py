"""
   action.py - a template file with unit tests implemenation of different
               action classes
"""
# HISTORY ####################################################################
#
# 0.0.1     Apr11   MR # The initial version of the file
##############################################################################
__description__ = "Unit tests for different Action classes"
__version__ = "0.0.1"
__author__ = "Miran R."

import unittest
import os
from pyrus.core.action import NoOpAction, ManualAction, ScriptedAction
from pyrus.core.action import ActionJsonDecoder

class NoOpActionUnit(unittest.TestCase):
    """
        NoOpActionUnit - class representing unit tests for NoOpAction
    """

    def setUp(self):
        self._act = NoOpAction() 

    def test_01_isAutomated(self):
        """Check isAutomated() method"""
        self.assertEqual(self._act.isAutomated(), True)

    def test_02_isScripted(self):
        """Check isScrited() method"""
        self.assertEqual(self._act.isScripted(), False)

    def test_03_str(self):
        """Check string representation"""
        self.assertEqual(str(self._act), "No action")

    def test_04_toJson(self):
        """Check the toJson() method"""
#        _json = """{"output": "", "description": "Empty Action", "rc": "0"}"""
        _json = "{}"
        self.assertEqual(self._act.toJson(), _json)


class ManualActionUnit(unittest.TestCase):
    """ 
        ManualActionUnit - class representing unit tests for ManualAction
    """

    def setUp(self):
        self._desc = "A manual action description"
        self._act = ManualAction(self._desc) 

    def test_01_isAutomated(self):
        """Checks isAutomated() method"""
        self.assertEqual(self._act.isAutomated(), False)

    def test_02_isScripted(self):
        """Checks isScrited() method"""
        self.assertEqual(self._act.isScripted(), False)

    def test_03_str(self):
        """Checks string representation"""
        _str_repr = "{} RC=0".format(self._desc)
        self.assertEqual(str(self._act), _str_repr)

    def test_04_toJson(self):
        """Check the toJson() method"""
        _j = """{{\n    "output": "", \n    "description": "{}", \n""".format(
                self._desc)
        _j += """    "rc": "0"\n}"""
        self.assertEqual(self._act.toJson(), _j)

    def test_05_description_get(self):
        """Check the description property"""
        self.assertEqual(self._act.description, self._desc)

    def test_06_description_set(self):
        """Check the description property - set operation"""
        _set = "A different manual action description"
        self._act.description = _set
        self.assertEqual(self._act.description, _set)

    def test_07_execute(self):
        """Check the return code after action has been executed"""
        self._act.execute()
        self.assertEqual(self._act.returncode, 0)

class ScriptedActionUnit(unittest.TestCase):
    """ 
        ScriptedActionUnit - class representing unit tests for ManualAction
    """

    def setUp(self):
#        self._script = os.path.abspath("scripts/hello.jar")
        self._script = "scripts/hello.jar"
        self._args = "arg1 arg2"
        self._act = ScriptedAction(self._script, self._args)

    def test_01_isAutomated(self):
        """Check isAutomated() method"""
        self.assertEqual(self._act.isAutomated(), True)

    def test_02_isScripted(self):
        """Check isScrited() method"""
        self.assertEqual(self._act.isScripted(), True)

    def test_03_script_prop(self):
        """Check the script property"""
        self.assertEqual(self._act.script, self._script)

    def test_04_args_prop(self):
        """Check the args property"""
        self.assertEqual(self._act.args, self._args)

    def test_05_str(self):
        """Check string representation"""
        _str_repr = "{} {}".format(self._script, self._args)
        self.assertEqual(str(self._act), _str_repr)

    def test_06_toJson(self):
        """Check the toJson() method"""
        #print(self._act.toJson())
        _json = """{{\n    "output": "", \n    "args": "{}", """.format(
                                                                    self._args)
        _json+= """\n    "rc": "-1", """
        _json += """\n    "script": "{}"\n}}""".format( self._script)
        self.assertEqual(self._act.toJson(), _json)

    def test_07_default_rc(self):
        """Check the execute method"""
        self.assertEqual(self._act.returncode, -1)

    def test_08_execute_rc_proper(self):
        """Check the RC after execute() method"""
        self._act.execute()
        self.assertEqual(self._act.returncode, 0)

    def test_09_execute_output_proper(self):
        """Check the RC after execute() method"""
        _out = "Hello World!\r\n"
        self._act.execute()
        self.assertEqual(self._act.output, _out)

    def test_10_execute_toJson(self):
        """Check the toJson() method after calling execute()"""
        #print(self._act.toJson())
        _json = """{\n    "output": "Hello World!\\r\\n", """
        _json += """\n    "args": "{}", """.format(self._args)
        _json += """\n    "rc": "0", """
        _json += """\n    "script": "{}"\n}}""".format(self._script)
        self._act.execute()
        self.assertEqual(self._act.toJson(), _json)

    def test_11_execute_str(self):
        """Check string representation after calling execute()"""
        _str_repr = "{} {}".format(self._script, self._args)
        self._act.execute()
        self.assertEqual(str(self._act), _str_repr)

def runtests():
    print(">>> Executing the 'NoOpAction unit tests...")
    suite = unittest.makeSuite(NoOpActionUnit)
    unittest.TextTestRunner(verbosity=2).run(suite)
    #
    print(">>> Executing the 'ManualAction unit tests...")
    suite = unittest.makeSuite(ManualActionUnit)
    unittest.TextTestRunner(verbosity=2).run(suite)
    #
    print(">>> Executing the 'ScriptedAction unit tests...")
    suite = unittest.makeSuite(ScriptedActionUnit)
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
    runtests()
