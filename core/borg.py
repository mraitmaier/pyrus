"""
    borg.py - script implementing Borg class
"""

class Borg(object):
    __shared_state = {}
    def __init__(self):
        self.__dict__ = self.__shared_state
        self.val = {}
