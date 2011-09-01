"""
    mongo.py - a MongoDB connector class
"""
from __future__ import print_function
from pymongo import Connection 

_DEF_MONGODB_HOST = "localhost"
_DEF_MONGODB_PORT = 27017
_DEF_MONGODB_NAME = "pyrus"

class MongoDbConnector(object):
    """
    """

    def __init__(self, dbname=_DEF_MONGODB_NAME, auto=False, 
                       host=_DEF_MONGODB_HOST, port=_DEF_MONGODB_PORT):
        """Ctor"""
        self._opened = False
        self._dbname = dbname
        self._host = host
        self._port = port
        self._dbconn = None  # a DB connection
        self._db = None      # a DB  itself
        if auto:
            self.open()

    @property
    def host(self):
        """MongoDB host (IP address)"""
        return self._host

    @property
    def port(self):
        """MongoDB port"""
        return self._port

    @property
    def dbName(self):
        """MongoDB database name"""
        return self._dbname

    @property
    def connection(self):
        """MongoDB Connection class instance"""
        return self._dbconn

    def open(self):
        """Open connection to MongoDB database and return a DB instance"""
        assert self.host is not None
        assert self.port is not None
        assert self.dbName is not None
        assert self.dbName is not ""
        self._dbconn = Connection(self.host, self.port)
        self._db = self._dbconn[self.dbName] 
        self._opened = True
        return self._db

    def close(self):
        """Close connection to MongoDB database"""
        assert self._dbconn is not None
        self._dbconn.disconnect()
        self._opened = False

    def isOpen(self):
        """check if MongoDB is open."""
        return self._opened

def runtests():
    print(">>> Starting tests...")
    conn = MongoDbConnector()
    db = conn.open()
    print("Connection opened: {}.".format(conn.isOpen()))
    print("  host: {}".format(conn.host))
    print("  port: {}".format(conn.port))
    print("  DB name: '{}'".format(conn.dbName))
    print("  connection: {}".format(str(conn.connection)))
    conn.close()
    print("Connection opened: {}.".format(conn.isOpen()))
    print(">>> Stop.")

if __name__ == "__main__":
    print(__doc__)
    runtests()
