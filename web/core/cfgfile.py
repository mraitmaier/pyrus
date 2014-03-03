#!/usr/bin/env python
'''
    cfgfile.py - 
'''
# HISTORY ####################################################################
#
# 1     MR  Feb14   Initial version
#
##############################################################################
from __future__ import print_function

_DEFAULT_CFG_FILE_PATH = './cfg/pyrusweb.cfg'

def read_config_file(filename=_DEFAULT_CFG_FILE_PATH):
    '''Reads the configuration file, parses the parameters and returns the
    parameters as a dictionary.'''
    assert filename is not None
    with open(filename) as fin:
        lines = fin.readlines()
    webcfg = dict() # configuration params are stored as a dict
    for l in lines:
        line = l.strip()
        if line == '' or line.startswith('#'):
            continue
        tokens = line.split('=')
        if len(tokens) != 2:
            continue
        # save the current configuration value 
        webcfg[tokens[0].strip()] = tokens[1].strip(' \t\n\'"')
    return webcfg

if __name__ == '__main__':
    print(__doc__)
    d = read_config_file()
    print(str(d))
