"""
File: DomainUtils.py
PUrpose:
Copywrite: Sendwell 2013
"""

import string

class DomainUtils(object):
    
    def RTypeToDBEnum(self,rType):
        retVal = str(rType)
        
    def removeEndingDots(self,name):
        if name.endswidth("."):
            name = name[:-1]
        return name