"""
   macaddress.py - module containing implementation of the MacAddress class

   NOTE: this module is not to be used standalone, except for testing purposes!
"""   
from __future__ import print_function

__description__ = "MAC address"
__version__ = "1.0"
__author__ = "Miran R."


# Broadcast MAC address definition (string)
BROADCAST_MAC = "ff:ff:ff:ff:ff:ff"
# bitmask to determine whether MAC address is multicast
_MULTICAST_MASK = 0x01

class MacAddressError(Exception):
    pass

class MacAddress(object):
    """
        MacAddress - class representing MAC address
    """

    def __init__(self, address):
        self.__address = address
        self._parse()
        if not self.isValid():
            raise MacAddressError("Invalid MAC address")

    def __str__(self):
        return self.address

    @property
    def address(self):
        return self.__address

    def toBytes(self):
        """Converts MAC from string into list of bytes."""
        bytes = list()
        temp = self.__address.split(":")
        cnt = 0                                    
        for chunk in temp:
            bytes.insert(cnt, int(chunk, 16))
            cnt = cnt + 1 
        return bytes        

    def _parse(self):
        """Parses the given MAC address and transforms it into 
        "xx:xx:xx:xx:xx:xx" form. 
        In general, class accepts three forms of MAC address input:
            - "1234567890af",
            - "12-34-56-78-90-af" (windows-like) and
            - "12:34:56:78:90:af" (the most used form).
        Class always works with the third form. 
        """      
        temp = self.__address
        if "-" in temp:
            temp = temp.replace("-", ":")
        if ":" not in temp:
            lst = list(temp)
            for cnt in range(10, 0, -2):
                lst.insert(cnt, ":")
            temp = ""
            for c in lst:
                temp = temp + c 
        self.__address = temp.lower()     

    def isBroadcast(self):
        """Checks whether MAC address is broadcast."""
        if self.__address == BROADCAST_MAC:
            return True
        return False

    def isMulticast(self):
        """Checks whether MAC address is multicast."""
        # we're interested only in first byte
        if self.isBroadcast():
            return False
        byte = int(self.__address.split(":")[0], 16)
        if byte & _MULTICAST_MASK:
            return True
        return False

    def isUnicast(self):
        """Checks whether MAC address is unicast."""
        return not(self.isBroadcast() or self.isMulticast())

    def isValid(self):
        """Checks whether MAC address is valid."""
        bytes = self.__address.split(":")
        if len(bytes) != 6:
            return False
        for byte in bytes:
            val = int(byte, 16)
            if val < 0 or val > 255:
                return False
        return True

# public functions, independent of the MacAddress class
def isValidMac(mac):
    """Checks whether MAC address is valid."""
    assert mac is not None
    bytes = mac.split(":")
    if len(bytes) != 6:
        return False
    for byte in bytes:
        val = int(byte, 16)
        if val < 0 or val > 255:
            return False
    return True

def isBroadcastMac(mac):
    """Checks whether MAC address is broadcast."""
    assert mac is not None
    if isValidMac(mac):
        if mac == BROADCAST_MAC:
            return True
    return False

def isMulticastMac(mac):
    """Checks whether MAC address is multicast."""
    # we're interested only in first byte
    assert mac is not None
    if isValidMac(mac):   
        if isBroadcastMac(mac):
            return False
        byte = int(mac.split(":")[0], 16)
        if byte & _MULTICAST_MASK:
            return True
    return False

def isUnicastMac(mac):
    """Checks whether MAC address is unicast."""
    assert mac is not None
    return not(isBroadcastMac(mac) or isMulticastMac(mac))

def toBytes(mac):
    """Converts MAC from string into list of bytes."""
    assert mac is not None
    bytes = [0,0,0,0,0,0]
    if isValidMac(mac):
        temp = mac.split(":")
        cnt = 0                                    
        for chunk in temp:
            bytes[cnt] = int(chunk, 16)
            cnt = cnt + 1 
    return bytes        

def toString(mac):
    """Converts a MAC address from list-of-integer-bytes form to string form."""
    assert mac is not None
    assert isinstance(mac, list)
    # if "mac" is not valid MAC address, None is returned.
    s = None
    # check MAC address bytes
    if len(mac) == 6:
        for byte in mac:
            if byte not in range(0, 256):
                return s
        # if everything is OK, create the MAC address string 
        s = "%02x:%02x:%02x:%02x:%02x:%02x" % (mac[0], mac[1], mac[2], 
                                             mac[3], mac[4], mac[5])
    return s

def parse(address):
    """Parses the given MAC address and transforms it into "xx:xx:xx:xx:xx:xx"
    form. This form of expressing MAC addresses is the most standard one.
    In general, the "address" parameter accepts three forms of MAC address i
    input:
        - '1234567890af',
        - '12-34-56-78-90-af' (windows-like) and
        - '12:34:56:78:90:af' (the most used form).
    The 'address' parameter must be string, of course.
    """      
    assert address is not None
    temp = address
    if "-" in temp:
        temp = temp.replace("-", ":")
    if ":" not in temp:
        lst = list(temp)
        for cnt in range(10, 0, -2):
            lst.insert(cnt, ":")
        temp = ""
        for c in lst:
            temp = temp + c 
    return temp.lower()     

# testing  ##################################################################
def test():
    print("### starting tests...")
    mac = MacAddress("1234567890af")
    print(str(mac))
    mac = MacAddress("12-34-56-78-90-af")
    print(str(mac))
    mac = MacAddress("12:34:56:78:90:af")
    print(str(mac))
    print(mac.isBroadcast())
    print(mac.isMulticast())
    print(mac.isUnicast())
    mac = MacAddress("01:34:56:78:90:af")
    print(mac.address)
    print(str(mac))
    print(mac.isBroadcast())
    print(mac.isMulticast())
    print(mac.isUnicast())
    print(mac.toBytes())
    mac = MacAddress("01:34:56:78:90:af")
    print(mac.address)
    print(str(mac))
    print(mac.isBroadcast())
    print(mac.isMulticast())
    print(mac.isUnicast())
    print(mac.toBytes())
    del mac
    print("### standalone functions")
    print(isValidMac("00:ff:ff:ff:ff:ff"))
    print(isValidMac("ff:ff:ff:ff:ff:ff"))
    print(isValidMac("01:ff:ff:ff:ff:ff"))
    print(isValidMac("01:ff:fff:ff:ff:ff"))
    print(isValidMac("01:ff:ff:ff:ff:fff"))
    print(isValidMac("01:ff:ff:ff:ff"))
    print("----------------")
    print(isBroadcastMac("00:ff:ff:ff:ff:ff"))
    print(isBroadcastMac("ff:ff:ff:ff:ff:ff"))
    print(isBroadcastMac("01:ff:ff:ff:ff:ff"))
    print("----------------")
    print(isMulticastMac("00:ff:ff:ff:ff:ff"))
    print(isMulticastMac("ff:ff:ff:ff:ff:ff"))
    print(isMulticastMac("01:ff:ff:ff:ff:ff"))
    print("----------------")
    print(isUnicastMac("00:ff:ff:ff:ff:ff"))
    print(isUnicastMac("ff:ff:ff:ff:ff:ff"))
    print(isUnicastMac("01:ff:ff:ff:ff:ff"))
    print("----------------")
    print(toBytes("01:ff:ff:ff:ff:ff"))
    print(toBytes("00:ff:ff:ff:ff:ff"))
    print(toBytes("ff:ff:ff:ff:ff:ff"))
    print(toBytes("fff:ff:ff:ff:ff:ff"))
    print("----------------")
    print(toString([0xff, 0xff, 0xff, 0xff, 0xff, 0xff]))
    print(toString([0xff, 0xff, 0xff, 0xff, 0xff, 0xff]))
    print(toString([0x0, 0xff, 0xff, 0xff, 0xff, 0xff]))
    print(toString([0x1, 0xff, 0xff, 0xff, 0xff, 0xff]))
    print(toString([0x1, 0xff, 0xff, 0xff, 0xfe, 0xf]))
    print(toString([0x1, 0xff, 0xff, 0xff, 0xfef, 0xf]))
    print("### end.")

if __name__ == "__main__":
    print(__doc__)
    test()
