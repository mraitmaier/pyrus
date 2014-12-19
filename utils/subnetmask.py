"""
   subnetmask.py - module that contains class for manipulating IP subnet
                   masks

   NOTE: this module should not be run as a standalone scripts, excepts for
   built-in tests.

"""


import sys, os
import iputils

__description__ = "a SubnetMask class implementation"
__version__ = "2"
__author__ = "Miran R."

# Define dictionary that represents possible mask values as keys and
# the appropriate number of bits they represent as values.
_MASK_VALS = { 0:0, 128:1, 192:2, 224:3, 240:4, 248:5, 252:6, 254:7, 255:8 }

class SubnetMask(object):
    """ 
    """

    def __init__(self, val, fromBits=False):
        """Ctor"""
        assert val is not None
        # if number of bits is given for mask, convert it to dotted value
        if fromBits:
            if val < 8 or val > 32:
                raise ValueError("Illegal number of bits for subnet mask.")
            self._bits = val 
            self._mask = self._dottedFromBits(val)
        # otherwise, we have a 
        else:
            assert self._check(val), "Invalid IP address"
            self._mask = val
            self._bits = self._bitsFromDotted(val)

    def __str__(self):
        return "{}".format(self._mask)

    @property
    def mask(self):
        """Returns a subnet mask value dotted notation"""
        return self._mask

    @property
    def bits(self):
        """Returns a subnet mask value as a number ob bits"""
        return self._bits

    def _dottedFromBits(self, bits):
        """Creates a subnet mask in dotted notation from number of bits."""
        assert bits > 0
        assert bits <= 32
        mask = "0" * 32
        mask = mask.replace("0", "1", bits)
        dot_mask = "{}.{}.{}.{}".format(int(mask[:8], 2), int(mask[8:16], 2),
                                        int(mask[16:24], 2), int(mask[24:], 2))
        return dot_mask

    def _bitsFromDotted(self, mask):
        """Returns the number of bits for a subnet in dotted notation."""
        assert mask is not None
        bits = 0 # default, serves as error value also
        if self._check(mask):
            lst = mask.split(".")
            for num in lst:
                bite = int(num)
                if bite in list(_MASK_VALS.keys()):
                    bits += _MASK_VALS[bite]
                else:
                    raise ValueError("subnet mask is not valid.")
        return bits

    def _check(self, val):   
        """Checks whether given IP subnet mask is valid or not.
        Implements only basic checking.
        """
        # turn dotted subnet into list of 4 strings
        mask_lst = val.split(".")
        # if length of the list is not 4, this is not valid subnet mask
        if len(mask_lst) != 4:
            return False
        # define valid values for subnet mask   
        valid_values = list(_MASK_VALS.keys())
        prev = 255
        for part in mask_lst:
            if part == "":
                return False
            num = int(part) # convert string into integer
            # mask values can take only selected values
            if num not in valid_values:
                return False
            # mask values must be continuous
            if prev < num:
                return False
            prev = num   
        # if all tests are passed, this is valid subnet mask   
        return True

    def toBytes(self):
        """Converts a dotted subnet mask into a list of bytes."""
        bytes = list()
        str_lst = self.mask.split(".")
        cnt = 0                                
        for part in str_lst:
            bytes.append(int(part))
            cnt = cnt + 1
        return bytes                

# TESTING ####################################################################

TEST_LIST_ERROR = ["255.255.255.255.255", "255.255.255", "255",
                   "234.234.234.234", "255.0.255.0",
                   "0.0.255.255", "255.255.255.1","254.255.255.254",
                   "255.255.256.0", "255.-255.255.0"] 

TEST_LIST_PROPER = ["255.255.255.255", "255.255.255.254", "255.255.255.252",
                    "255.255.255.248", "255.255.255.240", "255.255.255.224",
                    "255.255.255.192", "255.255.255.128", "255.255.255.0",
                    "255.255.254.0", "255.255.252.0", "255.255.248.0",
                    "255.255.240.0", "255.255.224.0", "255.255.128.0",
                    "255.255.0.0", "255.254.0.0", "255.252.0.0",
                    "255.248.0.0", "255.240.0.0", "255.224.0.0", 
                    "255.192.0.0", "255.128.0.0", "255.0.0.0", 
                    "254.0.0.0", "252.0.0.0", "248.0.0.0", 
                    "240.0.0.0", "224.0.0.0", "192.0.0.0", 
                    "128.0.0.0", "0.0.0.0"]                   
def run_tests():
    print("Starting tests...")
    print("#1 ## Ordinary test ##")
    msk = SubnetMask("255.255.255.0")
    print("Str(mask): {}".format(str(msk)))
    print("Get test: {}".format(msk.mask))
    print("Num of bits: {}".format(msk.bits))
    del msk
    print("#2 ## wrong mask test ##")
    for m in TEST_LIST_ERROR:                                
        try:                                
            print("Trying mask: {}... ".format(m), end=" ")
            mask = SubnetMask(m)
        except AssertionError as ex:
            print("{} OK".format(ex))
            continue
        else:
            print( "FAIL")
    print("#3 ## proper mask test ##")
    for m in TEST_LIST_PROPER:                                
        try:                                
            print("Trying mask: {}...".format(m), end=" ") 
            mask = SubnetMask(m)
        except AssertionError as ex:
            print("{} FAIL".format(ex))
            continue
        else:
            print( "OK")
            print(mask.mask)
            print(mask.bits)
            print(str(mask))
            print(mask.toBytes())
    print("#4 ## proper mask test from bits ##")
    for val in range(8, 33):
        print("Trying mask with {} bits...".format(val), end=" ")
        try:
            msk = SubnetMask(val, fromBits=True)
        except ValueError as ex:
            print(" FAIL {}".format(ex))
        else:
            print(" OK")
            print(msk.mask)
            print(msk.bits)
            print(str(msk))
    print("#5 ## invalid mask test from bits ##")
    for val in [0,1,2,3,4,5,6,7,33,34,35,36,666,999,-1,-15,-666,2.4]:
        print("Trying mask with {} bits...".format(val), end=" ")
        try:
            msk = SubnetMask(val, fromBits=True)
        except ValueError as ex:
            print(" OK {}".format(ex))
        else:
            print(" FAIL")
#    print("#4 ## proper mask test ##")
#    for i in _MASK_VALS.keys():
#        for j in _MASK_VALS.keys():
#            for k in _MASK_VALS.keys():
#                m = "255.{}.{}.{}".format(i,j,k)
#                print("Trying mask {}...".format(m), end=" ")
#                try:
#                    msk = SubnetMask(m)
#                except AssertionError as ex:
#                    print(" FAIL: {}".format(ex))
#                else:
#                    print(" OK")
    print("end.")

if __name__ == "__main__":
    print(__doc__)
    run_tests()
