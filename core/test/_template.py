"""
   _template.py - a  template file for creating unit tests

   The former is the main class (as the name of the file suggests...) and it
   is a container for test result. The latter is just a simple helper class
   serving as a enum for available test result values. It's convenient for
   importing and easy to use.

   NOTE: this module should not be run as a standalone scripts, excepts for
   built-in tests.
"""
# HISTORY ####################################################################
#
# 0.0.1     Apr11   MR # The initial version of the file
##############################################################################
__description__ = "_Template class implementation"
__version__ = "0.0.1"
__author__ = "Miran R."

import unittest

class _TemplateUnit(unittest.TestCase):
    """
        _TemplateUnit - class representing unit tests 
    """
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_01_pass(self):
        """ """
        s = 0
        self.assertEqual(s, 0)

if __name__ == '__main__':
    suite = unittest.makeSuite(_TemplateUnit)
    unittest.TextTestRunner(verbosity=2).run(suite)
