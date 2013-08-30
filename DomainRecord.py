"""
File: DomainRecord.py
purpose: Object
Copywrite: Sendwell 2013
"""

import re

class DomainRecord(object):
    def getRefresh(self):
        return self.refresh;
    
    def setRefresh(self,refresh):
        self.refresh = refresh
        
    def getTTL(self):
        return self.TTL
    
    def setTTL(self,ttl):
        self.TTL = ttl

    def getMinimum(self):
        return self.minimum
    
    def setMinimum(self,minimum):
        self.minimum = minimum
        
    def getID(self):
        return self.ID
    
    def setID(self,ID):
        self.ID = ID
    
    def getRetry(self):
        return self.retry
    
    def setRetry(self,retry):
        self.retry = retry
    
    def getOrigin(self):
        return self.origin;
    
    def setOrigin(self,origin):
        self.origin = origin
        
    def getExpire(self):
        return self.expire
    
    def setExpire(self,expire):
        self.expire = expire
        
    def getLastCheck(self):
        return self.lastcheck
    
    def setLastCheck(self,lastcheck):
        self.lastcheck = lastcheck
        
    def getLocked(self):
        return self.locked
    
    def setLocked(self,locked):
        self.locked = locked
                
    def toString(self):
        return "ID\t%s\nOrigin\t%s\nRefresh\t%s\nRetry\t%s\nExpire\t%s\nMinimum\t%s\nTTL\t%s\nLast Check\t%s\nLocked\t%s\n" % (self.getID(),self.getOrigin(),self.getRefresh(),self.getRetry(),self.getExpire(),self.getMinimum(),self.getTTL(),self.getLastCheck(),self.getLocked())

    def __init__(self,ID,origin="",minimum=0,TTL=0,refresh=0,retry=0,expire=0,lastcheck=0,locked=False):
        self.minimum = minimum
        self.TTL = TTL
        self.refresh = refresh
        self.origin = origin
        self.ID = ID
        self.retry = retry
        self.expire = expire
        self.lastcheck = lastcheck
        self.locked = locked
        
        
        