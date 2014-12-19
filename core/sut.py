"""
   sut.py - 

   NOTE: this module should not be run as a standalone scripts, excepts for
   built-in tests.

"""
# HISTORY ####################################################################
#                       
#  1 Mar11   MR # Initial version
#  2 Dec14   MR # Ported to Py3
#                       
##############################################################################


__description__ = "a SystemUnderTest class implementation"
__version__ = "2"
_author__ = "Miran R."

import json
from pyrus.core.enum import enum

SUTType = enum(["UNKNOWN", "HARDWARE", "SOFTWARE", "BOTH"])

def toSUTType(str_val):
    str_val = str_val.lower()
    if str_val in ["hw", "hardware"]:
        return SUTType.HARDWARE
    elif str_val in ["sw", "software"]:
        return SUTType.SOFTWARE
    else:
        return SUTType.UNKNOWN

class SystemUnderTest(object):
    """
        SystemUnderTest -
    """

    def __init__(self, name, suttype=SUTType.UNKNOWN, version=None,
                             ip="0.0.0.0", description=""):
        self._name = name
        self._type = suttype
        self._version = version
        self._description = description
        self._ip = ip

    def __str__(self):
        s = "\n".join(("SUT: {}".format(self.name),
                       "  type: {}".format(self.typeToString()),
                       "  version: {}".format(self.version),
                       "  IP address: {}".format(self.ip),
                       "  description:\n{}".format(self.description)
                  ))
        return s

    @property    
    def name(self):
        return self._name

    @property
    def suttype(self):
        return self._type

    @property
    def version(self):
        return self._version

    @property
    def ip(self):
        return self._ip

    @property
    def description(self):
        return self._description

    def typeToString(self):
        if self.suttype == SUTType.UNKNOWN:
            return "unknown"
        elif self.suttype == SUTType.HARDWARE:
            return "hardware"
        elif self.suttype == SUTType.SOFTWARE:
            return "software"
        else:
            return "test object value error"

    def toJson(self):
        return json.dumps(self, indent=4, cls=_SutJsonEncoder)

    def toXml(self):
        n = """<SystemUnderTest name="{}">\n""".format(self.name)
        t = "<Type>{}</Type>".format(self.typeToString())
        v = "<Version>{}</Version>".format(self.version)
        i = "<IP>{}</IP>\n".format(self.ip)
        d = "<Description>{}</Description>\n".format(self.description)
        return "".join((n, t, v, i, d, "</SystemUnderTest>\n"))

    def toHtml(self, cssClass=None):
        """Return the HTML respresentation of the class instance."""
        if cssClass:
            d = """<div id="sut" class="{}">""".format(cssClass)
        else:
            d = """<div id="sut">"""
        n = "<b>System Under Test:</b> {}<br>".format(self.name)
        t = "<i>Type:</i> {}<br>".format(self.typeToString())
        v = "<i>Version:</i> {}<br>".format(self.version)
        i = "<i>IP Address:</i> {}<br>".format(self.ip)
        dsc ="<i>Description:</i> {}".format(self.description)
        return "\n".join((d, n, t, v, i, "</div>"))

class _SutJsonEncoder(json.JSONEncoder):
    """ """

    def default(self, obj):
        if isinstance(obj, SystemUnderTest):
            d = dict()
            if hasattr(obj, "name"):
                d["name"] = obj.name
            if hasattr(obj, "suttype"):
                d["type"] = obj.typeToString()
            if hasattr(obj, "version"):
                d["version"] = obj.version
            if hasattr(obj, "ip"):
                d["ip"] = obj.ip
            if hasattr(obj, "description"):
                d["description"] = obj.description
            return d
        return json.JSONEncoder(obj)

class SutJsonDecoder(json.JSONDecoder):
    """ """
    def decode(self, jsontext):
        # we convert JSON text into python dictionary
        sutDict = json.loads(jsontext)
        # define default values
        name = "Untitled SUT"
        version = "x.y"
        ip = "0.0.0.0"
        suttype = SUTType.UNKNOWN
        desc = ""
        #
        if "name" in sutDict:
            name = sutDict["name"]
        if "type" in sutDict:
            suttype = toSUTType(sutDict["type"])
        if "ip" in sutDict:
            ip = sutDict["ip"]
        if "version" in sutDict:
            version = sutDict["version"]
        if "description" in sutDict:
            desc = sutDict["description"]
        return SystemUnderTest(name, suttype, version, ip, desc)

 # TESTING ####################################################################
def runtests():
    print("Starting unit tests...")
    to = SystemUnderTest("a system under test", SUTType.HARDWARE, "1.0",
                         "192.168.1.2", "This is a description")
    print(str(to))
    j = to.toJson()
    print(j)
    s = SutJsonDecoder().decode(j)
    print("type: {}\ndata='{}'".format(type(s), str(s)))
    print("XML={}".format(s.toXml()))
    print("HTML={}".format(s.toHtml()))
    print("Stop")

if __name__ == '__main__':
   print(__doc__)
   runtests()
