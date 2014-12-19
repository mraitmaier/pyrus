"""
   ip_address.py - module that contains class for manipulating IP addresses

   NOTE: this module should not be run as a standalone scripts, excepts for
   built-in tests.

"""

import sys, os

__description__ = "IP address"
__version__ = "2"
__author__ = "Miran R."

LOCALHOST = "127.0.0.1"
LOOPBACK = "127.0.0.1"    # reserved IP address for loopback interface
LOOPBACK_HEX = "7F000001" # loopback interface hex representation

class IpAddress(object):
   """
         IpAddress - class implementing IP address manipulation
   """      
   def __init__(self, ip):
      """Ctor."""
      assert self._check(ip), "Invalid IP address"
      self._ip = ip   

   def __str__(self):
      return self._ip

   @property
   def address(self):
      """Address property getter"""
      return self._ip

   def _check(self, addr):
      """Check the validity of the given IP address"""
      # split address in dotted notation into list of four strings
      addr_lst = addr.split(".")
      # if length of the list is not 4, this is not valid address
      if len(addr_lst) != 4:
         return False   
      # check all parts of the IP address for values   
      for part in addr_lst:
         if part == "":
            return False
         num = int(part)
         if num < 0 or num > 255:
            return False
      # if all tests are passed, this is valid IP address   
      return True   
     
   def toBytes(self):
      """Returns the IP address value as a list of bytes"""
      # check if IP address is defined; if not raise ValueError
      addr_lst = list()                  
      # split an address into list 
      lst = self._ip.split(".")
      for part in lst:
         addr_lst.append(int(part)) # convert string to integer
      return addr_lst   

   def toHex(self, prefixed=True):
      """
      Returns an IP address as a Hex string representation. The 'prefixed' optional parameters defines whether hex value
      should be prefixed with '0x'. True by default.
      """
      # set hex prefix   
      hx = ""
      if prefixed:
         hx = "0x"
      # convert IP addres in dotted notation into list of bytes
      bytes = self.toBytes()
      # for every number in address integer list...
      for num in bytes:
         # Add string hex representation of the current integer:
         # 1. convert integer to hex string,
         # 2. strip the leading '0x', 
         # 3. zero-fill it to 2 characters and
         # 4. force lowercase
         hx = hx + hex(num).lstrip("0x").zfill(2).lower() 
      return hx

   def isUnicast(self):
      """Checks if IP address is the unicast one."""
      status = False
      lst = self._ip.split(".")
      if int(lst[0]) in range(224):
          status = True
      return status 

   def isMulticast(self):
      """Checks if IP address is the multicast one."""
      status = False
      lst = self._ip.split(".")
      if int(lst[0]) in range(224, 239):
          status = True
      return status 

   def isExperimental(self):
      """Checks if IP address is the experimental one."""
      status = False
      lst = self._ip.split(".")
      if int(lst[0]) in range(240, 256):
          status = True
      return status 

   def isPrivate(self):
      """Checks if IP address is from the private range"""
      status = False
      lst = self._ip.split(".")
      if int(lst[0]) in [10, 172, 192]:
          status = True
      return status 

# TESTING ####################################################################
def run_tests():
   print("Starting tests...")
   ip = IpAddress("192.168.180.1")
   print(("IP: %s" % ip.address))
   print(("Hex (with prefix): %s" % ip.toHex()))
   print(("Hex (without prefix): %s" % ip.toHex(False)))
   print(("Unicast? {}".format(ip.isUnicast())))
   print(("Multicast? {}".format(ip.isMulticast())))
   print(("Private? {}".format(ip.isPrivate())))
   print(("Experimental? {}".format(ip.isExperimental())))
   print((str(ip)))
   del ip
   print("### test")
   ip = IpAddress(LOOPBACK)
   print(("IP: %s" % ip.address))
   print(("Hex (with prefix): %s" % ip.toHex()))
   print(("Hex (without prefix): %s" % ip.toHex(False)))
   print((str(ip)))
   del ip
   print("### test")
   try:
      ip = IpAddress("192.168.2.3.4")
   except AssertionError as ex:
      print(("Assertion caught: {}".format(ex)))
   else:
      print("Did not caught exception: Fail")
   print("### test")
   try:
      ip = IpAddress("192.168.333.4")
   except AssertionError as ex:
      print(("Assertion caught: {}".format(ex)))
   else:
      print("Did not caught exception: Fail")
   print( "### test")
   ip = IpAddress("172.16.15.33")
   print(("IP: {}".format(ip.address)))
   print(("Hex (with prefix): {}".format(ip.toHex())))
   print(("Hex (without prefix): {}".format(ip.toHex(False))))
   print(("Unicast? {}".format(ip.isUnicast())))
   print(("Multicast: {}".format(ip.isMulticast())))
   print(("Private? {}".format(ip.isPrivate())))
   print(("Experimental? {}".format(ip.isExperimental())))
   print( "### test")
   ip = IpAddress("224.16.15.33")
   print(("IP: {}".format(ip.address)))
   print(("Hex (with prefix): {}".format(ip.toHex())))
   print(("Hex (without prefix): {}".format(ip.toHex(False))))
   print(("Unicast? {}".format(ip.isUnicast())))
   print(("Multicast? {}".format(ip.isMulticast())))
   print(("Private? {}".format(ip.isPrivate())))
   print(("Experimental? {}".format(ip.isExperimental())))
   print( "### test")
   ip = IpAddress("242.16.15.33")
   print(("IP: {}".format(ip.address)))
   print(("Hex (with prefix): {}".format(ip.toHex())))
   print(("Hex (without prefix): {}".format(ip.toHex(False))))
   print(("Unicast? {}".format(ip.isUnicast())))
   print(("Multicast? {}".format(ip.isMulticast())))
   print(("Private? {}".format(ip.isPrivate())))
   print(("Experimental? {}".format(ip.isExperimental())))
   print("End.")

if __name__ == '__main__':
   print(__doc__)
   run_tests()
