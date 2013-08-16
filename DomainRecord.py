"""
File: DomainRecord.py
purpose: Object
Copywrite: Sendwell 2013
"""

import re
import DomainUtils

class DomainRecord(object):
    def getType(self):
        return self.type;
    
    def setType(self,uType):
        self.type = uType
        
    def getTTL(self):
        return self.ttl
    
    def setTTL(self,ttl):
        self.TTL = ttl

    def getAUX(self):
        return self.AUX
    
    def setAUX(self,aux):
        self.AUX = aux
        
    def getID(self):
        return self.ID
    
    def setID(self,ID):
        self.ID = ID
        
    def getRecordID(self):
        return self.recordID
    
    def getData(self):
        return self.data
    
    def setData(self,data):
        self.data = data
    
    def getName(self):
        return self.name;
    
    def setName(self,name):
        self.name = name
    
    class Builder(object):
        def __init__(self,domainRecord):
            self.DomainRecord = domainRecord
            
        def build(self):
            return self.DomainRecord
        
        def setAUX(self,aux):
            self.DomainRecord.setAUX = aux
            
        def setTTL(self,ttl):
            self.DomainRecord.setTTL = ttl
            
        def setType(self,uType):
            self.DomainRecord.setType = uType
            
        def setData(self,data):
            self.DomainRecord.setData = data
            
        def setName(self,name):
            self.DomainRecord.setName = name
            
    
    def builder(self,recordID):
        return self.Builder(DomainRecord(recordID))

    def getKey(self):
        return self.data+"/"+self.AUX+"/"+self.type
                
    def toString(self):
        return self.getType()+"\t"+self.data+"\t"+str(self.TTL)+"\t"

    def fromRecord(self,record):
        aux = 0
        data = DomainUtils.DomainUtils.removeEndingDots(record)
        
        pattern = re.compile('([0-9]+) (.*)')
        if pattern.match(data):
            aux = pattern.group(1)
            data = pattern.group(2)

        domainRecord = DomainRecord(0)
        domainRecord.setName(DomainUtils.DomainUtils.removeEndingDots(record.getName().toString()))
        domainRecord.setData(data)
        domainRecord.setAUX(aux)
        domainRecord.setTTL(record.getTTL())
        domainRecord.setType(record.getType())
        
        return domainRecord

    def __init__(self,recordID):
        self.recordID = recordID
        self.data = ""
        self.AUX = 0
        self.TTL = 0
        self.type = ""
        self.name = ""
        self.ID = 0
        