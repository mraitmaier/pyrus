"""\
    iputils.py -

"""
import sys, re, os

NAME = "IP utils"
VERSION = "2."
AUTHOR = "Miran R."

PLATFORM = sys.platform

# Define dictionary that represents possible mask values as keys and 
# the appropriate number of bits they represent as values.
MASK_VALS = { 0:0, 128:1, 192:2, 224:3, 240:4, 248:5, 252:6, 254:7, 255:8 }

def ping(host, num=1, timeout=None):
    """This is ping utility: runs a ping utility for a given platform
    and check if a given host is alive.
    Returns True if alive, otherwise False.
    Mandatory parameter is only host IP address. 
    There are 2 optional parameters:
    - num     - number of ICMP echo packets (pings) to be sent and
    - timeout - ICMP echo (ping) reply timeout (in miliseconds)
    """
    status = False
    if PLATFORM == "win32" or PLATFORM == "cygwin":
        status = _win32ping(host, num, timeout)
    elif PLATFORM == "linux2":
        status = _linuxping(host, num, timeout)
    return status
def _win32ping(host, num=1, timeout=None):
    """Windows version of ping function."""
    reply = re.compile(r'^Reply from.+bytes.+time.+TTL.+$')  # English version
    antw  = re.compile(r'^Antwort von.+Bytes.+Zeit.+TTL.+$') # German version
    # prepare ping command
    cmd = 'ping %s -n %s' % (host, str(num)) 
    if timeout is not None and int(timeout) > 0:
        cmd = cmd + '-w %s' % str(timeout)
    # run ping 
    ping = os.popen(cmd, 'r')
    sys.stdout.flush()
    lines = ping.readlines()
    replied = False
    for line in lines:
        if reply.search(line) is not None or \
           antw.search(line) is not None:
            replied = True
#    print '#DEBUG replied = ' + str(replied) # DEBUG
    return replied
def _linuxping(host, num=1, timeout=None):    
    """Linux version of ping function."""
    # prepare command
    reply = re.compile(r"^.+bytes from.+icmp_seq.+ttl.+time.+$") 
    cmd = "ping -c%s %s" % (num, host)
    # run ping
    ping = os.popen(cmd, "r")
    sys.stdout.flush()
    lines = ping.readlines()
    replied = False
    for line in lines:
        if reply.search(line) is not None:
            replied = True
#    print '#DEBUG replied = ' + str(replied) # DEBUG
    return replied
def check_ip(ip):
    """Checks whether given IP address is valid or not.
    Implements only basic checking."""
    if ip is not None:
        iplst = ip.split('.')
        if len(iplst) != 4:
            return False
        for num in iplst:
            if int(num) > 255 or int(num) < 0:
                return False
    return True    
def mask_dotted_from_bits(bits):
   """Creates a subnet mask string in dotted notation from number of bits."""
   assert bits > 0 
   assert bits <= 32
   mask = '0' * 32
   mask = mask.replace('0', '1', bits)
   dot_mask = '%s.%s.%s.%s' % ( int(mask[:8], 2), int(mask[8:16], 2),
                                int(mask[16:24], 2), int(mask[24:], 2) )
   return dot_mask
def mask_bits_from_dotted(mask):
   """Returns the number of bits for a subnet in dotted notation."""
   assert mask is not None
   bits = 0 # default, serves as error value also
   if check_mask(mask):
      lst = mask.split('.')
      for num in lst:
         bla = int(num)
         if bla in list(MASK_VALS.keys()):
            bits += MASK_VALS[bla]
         else:
            raise ValueError("ERROR: subnet mask is not valid.")
   return bits
def check_mask(mask):
   """ Checks whether given IP subnet mask is valid or not.
   Implements only basic checking.
   """
   # make a list from dotted subnet mask
   lst = mask.split('.')
   # if list length is not equal to 4, this is invalid
   if len(lst) != 4:
      return False
   # check for list for valid values   
   for num in lst:
      if int(num) not in list(MASK_VALS.keys()):
         return False
   # check continuousness of the list       
   import copy
   sorted = copy.copy(lst) # make a shalow copy of the list      
   sorted.sort(reverse=True) # and sort (actually reverse) it
   if lst != sorted:
      return False
   return True    

if __name__ == '__main__':
   print(__doc__)
