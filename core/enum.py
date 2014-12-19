"""
    enum.py - the implementation of the enums based on frozenset

NOTE: this script is not to be used standalone (except for testing), import it.
"""

AUTHOR = "Miran R."
VERSION = "1.0"
NAME = "enumeration implementation"

class enum(frozenset):
    """The simplest class-based implemenatation of enums in python that I'm
    aware of."""

    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError("Unknown value: {}".format(name))

if __name__ == "__main__":
    print(__doc__)
    print("Testing...")
    TestStatus = enum(("PASS", "FAIL", "XFAIL", "NOT_TESTED", "UNKNOWN"))
    print(TestStatus)
    print((str(TestStatus)))
    print((repr(TestStatus)))
    print((TestStatus.PASS))
    print((TestStatus.FAIL))
    assert TestStatus.PASS != TestStatus.FAIL
    assert TestStatus.PASS in TestStatus
    print("###")
    x = TestStatus.PASS
    print(x)
    if "PASS" in TestStatus:
        print("Hura for PASS!")
    if TestStatus.XFAIL in TestStatus:
        print("Hura for expected fail!")
    if "BLAH" not in TestStatus:
        print("Boooo for Blah!")
    try:
        y = TestStatus.BLAH
    except AttributeError as exc:
        print(("ERROR: {}".format(exc)))
    print("It's iterable!")
    for v in TestStatus:
        print(v)
