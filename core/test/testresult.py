"""
   testresult.py - a script implementing TestResult and TestStatus classes

   The former is the main class (as the name of the file suggests...) and it
   is a container for test result. The latter is just a simple helper class
   serving as a enum for available test result values. It's convenient for
   importing and easy to use.

   NOTE: this module should not be run as a standalone scripts, excepts for
   built-in tests.
"""
# HISTORY ####################################################################
#
# 0.0.1     Mar11   MR # The initial version of the file
##############################################################################
__description__ = "TestResult class implementation"
__version__ = "0.0.1"
__author__ = "Miran R."

import unittest
from pyrus.core.testresult import TestResult, TestStatus

class TestStatusUnit(unittest.TestCase):
    """
        TestStatusUnit - class representing unit tests for TestStatus class 
    """

    def test_01_pass(self):
        """ """
        s = TestStatus.PASS
        self.assertEqual(s, TestStatus.PASS)

    def test_02_pass(self):
        """ """
        s = 0
        self.assertEqual(s, TestStatus.PASS)

    def test_03_pass(self):
        """ """
        s = TestStatus.FAIL
        self.assertEqual(s, TestStatus.FAIL)

    def test_04_fail(self):
        """ """
        s = 1
        self.assertEqual(s, TestStatus.FAIL)

    def test_05_xfail(self):
        """ """
        s = TestStatus.XFAIL
        self.assertEqual(s, TestStatus.XFAIL)

    def test_06_xfail(self):
        """ """
        s = 2
        self.assertEqual(s, TestStatus.XFAIL)

    def test_07_nottested(self):
        """ """
        s = TestStatus.NOT_TESTED
        self.assertEqual(s, TestStatus.NOT_TESTED)

    def test_08_nottested(self):
        """ """
        s = 3
        self.assertEqual(s, TestStatus.NOT_TESTED)

    def test_09_skipped(self):
        """ """
        s = TestStatus.SKIPPED
        self.assertEqual(s, TestStatus.SKIPPED)

    def test_10_skipped(self):
        """ """
        s = 4
        self.assertEqual(s, TestStatus.SKIPPED)

    def test_11_unknown(self):
        """ """
        s = TestStatus.UNKNOWN
        self.assertEqual(s, TestStatus.UNKNOWN)

    def test_12_unknown(self):
        """ """
        s = -1
        self.assertEqual(s, TestStatus.UNKNOWN)

    def test_13_invalid(self):
        """ """
        s = -2
        self.assertNotIn(s, TestStatus.values, "Not in valid range")

    def test_14_invalid(self):
        """ """
        s = 5
        self.assertNotIn(s, TestStatus.values, "Not in valid range")

    def test_15_invalid(self):
        """ """
        s = 666
        self.assertNotIn(s, TestStatus.values, "Not in valid range")

    def test_16_invalid_str(self):
        """ """
        s = "blah" 
        self.assertNotIn(s, TestStatus.values, "Not in valid range")

    def test_17_invalid_float(self):
        """ """
        s = 0.23
        self.assertNotIn(s, TestStatus.values, "Not in valid range")

    def test_20_convert_pass(self):
        """ """
        vals = ["pass", "PASS", "PasS", "pASs", "    pass    ", " PASS", 
                " PasS    "]
        for v in vals:
            s = TestStatus.convert(v)
            self.assertEqual(s, TestStatus.PASS)

    def test_21_convert_fail(self):
        """ """
        vals = ["fail", "FAIL", "Fail", "fAIl", "    fail    ", " FaIL    "]
        for v in vals:
            s = TestStatus.convert(v)
            self.assertEqual(s, TestStatus.FAIL)

    def test_22_convert_xfail(self):
        """ """
        vals = ["xfail", "XFAIL", "xFail", "XfAIl", "    xfail    ", 
                " xFaIL    ", "expected fail", "EXPECTED FAIL", 
                "  EXpEcTED fAIL     "]
        for v in vals:
            s = TestStatus.convert(v)
            self.assertEqual(s, TestStatus.XFAIL)

    def test_23_convert_nottested(self):
        """ """
        vals = ["not tested", "NOT TESTED", "not_tested", "NOT_TESTED", 
                "    NOt_tested    ", " NOT tested    "]
        for v in vals:
            s = TestStatus.convert(v)
            self.assertEqual(s, TestStatus.NOT_TESTED)

    def test_24_convert_skipped(self):
        """ """
        vals = ["skipped", "SKIPPED", "SkiPPed", "    skipped    ", 
                "  SkiPpEd     "]
        for v in vals:
            s = TestStatus.convert(v)
            self.assertEqual(s, TestStatus.SKIPPED)

    def test_25_convert_unknown(self):
        """ """
        vals = ["unknownd", "UNKNOWN", "UnkNOwn", "    unknown   ", 
                "  UNKnown     "]
        for v in vals:
            s = TestStatus.convert(v)
            self.assertEqual(s, TestStatus.UNKNOWN)

    def test_26_convert_empty(self):
        """ """
        s = TestStatus.convert("")
        self.assertEqual(s, TestStatus.UNKNOWN)

    def test_27_convert_default(self):
        """ """
        s = TestStatus.convert("blah")
        self.assertEqual(s, TestStatus.UNKNOWN)

class TestResultUnit(unittest.TestCase):
    """
        TestResultUnit - represents unit tests for TestResult class
    """

    def test_01_pass(self):
        """ """
        r = TestResult(0)
        self.assertEqual(r.result, TestStatus.PASS)

    def test_02_pass(self):
        """ """
        r = TestResult(TestStatus.PASS)
        self.assertEqual(r.result, TestStatus.PASS)

    def test_03_pass_str(self):
        """ """
        r = TestResult(TestStatus.PASS)
        self.assertEqual(str(r), "pass")

    def test_04_pass_toJson(self):
        json = """{"result": "pass"}"""
        r = TestResult(TestStatus.PASS)
        self.assertEqual(r.toJson(), json)

    def test_05_fail(self):
        """ """
        r = TestResult(1)
        self.assertEqual(r.result, TestStatus.FAIL)

    def test_06_fail(self):
        """ """
        r = TestResult(TestStatus.FAIL)
        self.assertEqual(r.result, TestStatus.FAIL)

    def test_07_fail_str(self):
        """ """
        r = TestResult(TestStatus.FAIL)
        self.assertEqual(str(r), "fail")

    def test_08_fail_toJson(self):
        json = """{"result": "fail"}"""
        r = TestResult(TestStatus.FAIL)
        self.assertEqual(r.toJson(), json)

    def test_09_xfail(self):
        """ """
        r = TestResult(2)
        self.assertEqual(r.result, TestStatus.XFAIL)

    def test_10_xfail(self):
        """ """
        r = TestResult(TestStatus.XFAIL)
        self.assertEqual(r.result, TestStatus.XFAIL)

    def test_11_xfail_str(self):
        """ """
        r = TestResult(TestStatus.XFAIL)
        self.assertEqual(str(r), "expected fail")

    def test_12_xfail_toJson(self):
        json = """{"result": "expected fail"}"""
        r = TestResult(TestStatus.XFAIL)
        self.assertEqual(r.toJson(), json)

    def test_13_nottested(self):
        """ """
        r = TestResult(3)
        self.assertEqual(r.result, TestStatus.NOT_TESTED)

    def test_14_nottested(self):
        """ """
        r = TestResult(TestStatus.NOT_TESTED)
        self.assertEqual(r.result, TestStatus.NOT_TESTED)

    def test_15_nottested_str(self):
        """ """
        r = TestResult(TestStatus.NOT_TESTED)
        self.assertEqual(str(r), "not tested")

    def test_16_nottested_toJson(self):
        json = """{"result": "not tested"}"""
        r = TestResult(TestStatus.NOT_TESTED)
        self.assertEqual(r.toJson(), json)

    def test_17_skipped(self):
        """ """
        r = TestResult(4)
        self.assertEqual(r.result, TestStatus.SKIPPED)

    def test_18_skipped(self):
        """ """
        r = TestResult(TestStatus.SKIPPED)
        self.assertEqual(r.result, TestStatus.SKIPPED)

    def test_19_skipped_str(self):
        """ """
        r = TestResult(TestStatus.SKIPPED)
        self.assertEqual(str(r), "skipped")

    def test_20_skipped_toJson(self):
        json = """{"result": "skipped"}"""
        r = TestResult(TestStatus.SKIPPED)
        self.assertEqual(r.toJson(), json)

    def test_21_unknown(self):
        """ """
        r = TestResult(-1)
        self.assertEqual(r.result, TestStatus.UNKNOWN)

    def test_22_unknown(self):
        """ """
        r = TestResult(TestStatus.UNKNOWN)
        self.assertEqual(r.result, TestStatus.UNKNOWN)

    def test_23_unknown_str(self):
        """ """
        r = TestResult(TestStatus.UNKNOWN)
        self.assertEqual(str(r), "unknown")

    def test_24_unknown_toJson(self):
        json = """{"result": "unknown"}"""
        r = TestResult(TestStatus.UNKNOWN)
        self.assertEqual(r.toJson(), json)

    def test_25_default(self):
        """ """
        r = TestResult()
        self.assertEqual(r.result, TestStatus.UNKNOWN)

    def test_26_default_str(self):
        """ """
        r = TestResult()
        self.assertEqual(str(r), "unknown")

    def test_27_default_toJson(self):
        json = """{"result": "unknown"}"""
        r = TestResult()
        self.assertEqual(r.toJson(), json)

    def test_28_set(self):
        """ """
        r = TestResult()
        self.assertEqual(r.result, TestStatus.UNKNOWN)
        r.result = TestStatus.PASS
        self.assertEqual(r.result, TestStatus.PASS)
        r.result = TestStatus.FAIL
        self.assertEqual(r.result, TestStatus.FAIL)
        r.result = TestStatus.XFAIL
        self.assertEqual(r.result, TestStatus.XFAIL)
        r.result = TestStatus.SKIPPED
        self.assertEqual(r.result, TestStatus.SKIPPED)
        r.result = TestStatus.NOT_TESTED
        self.assertEqual(r.result, TestStatus.NOT_TESTED)
        r.result = TestStatus.PASS
        self.assertEqual(r.result, TestStatus.PASS)
        self.assertEqual(str(r), "pass")

    def test_29_invalid_below(self):
        """ """
        self.assertRaises(AssertionError, TestResult, -2)

    def test_30_invalid_above(self):
        """ """
        self.assertRaises(AssertionError, TestResult, 666)

    def test_31_invalid_float(self):
        """ """
        self.assertRaises(AssertionError, TestResult, 2.23)

    def test_32_invalidi_hex(self):
        """ """
        self.assertRaises(AssertionError, TestResult, 0x45)

    def test_33_invalid_string(self):
        """ """
        self.assertRaises(AssertionError, TestResult, "a string")

    def test_34_invalid_list(self):
        """ """
        self.assertRaises(AssertionError, TestResult, [])

    def test_35_invalid_dict(self):
        """ """
        self.assertRaises(AssertionError, TestResult, {})

if __name__ == '__main__':
    suite = unittest.makeSuite(TestStatusUnit)
    unittest.TextTestRunner(verbosity=2).run(suite)
    #
    suite = unittest.makeSuite(TestResultUnit)
    unittest.TextTestRunner(verbosity=2).run(suite)
