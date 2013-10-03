"""
File : DomainRecord.py
purpose: Object
Copywrite: Sendwell 2013
"""

import re
import DomainMX
import MXLockClasses

class DomainRecord(object):
    
    def setMX(self,ID,machine,priority,address,rType):
        mx = DomainMX.DomainMX(ID,machine,priority,address,rType)
        self.mx[ID] = mx
        
    def getMX(self,rrID):
        try:
            if rrID in self.mx:
                return self.mx[rrID]
        except KeyError as e:
            print "DomainRecord error: %s" % (e)
            
    def getNextMXID(self):
        mx = None
        if self.mx.__len__() > 0:
            print "MX Length: %s  Current Pos: %s" % (self.mx.__len__(),self.curPos)
            mx = self.mx.keys()[self.curPos]
            self.curPos = MXLockClasses.getNextCurPos(self.mx, self.curPos)
        return mx
        
    def getRefresh(self):
        return self.refresh
    
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

    def exists(self,ID):
        try:
            if ID in self.mx:
                return True
            else:
                return False
        except KeyError as e:
            print "DomainRecord error: %s" % (e)
                
    def toString(self):
        results = "ID\t%s\nOrigin\t%s\nRefresh\t%s\nRetry\t%s\nExpire\t%s\nMinimum\t%s\nTTL\t%s\nLast Check\t%s\nLocked\t%s\n" % (self.getID(),self.getOrigin(),self.getRefresh(),self.getRetry(),self.getExpire(),self.getMinimum(),self.getTTL(),self.getLastCheck(),self.getLocked())
        for key in self.mx:
            results += self.mx[key].toString()
        return results
    
    def getMXLength(self):
        return self.mx.__len__()

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
        
        self.mx = {}
        self.curPos = 0
        
        
        