"""
File: Domain.py
Purpose:
Copywrite: Sendwell 2013
"""

class Domain(object):
    
    def getTimeStamp(self):
        return self.timestamp
    
    def getIDNName(self):
        return self.IDNName
    
    def getDomainID(self):
        return self.domainID
    
    def getDomainName(self):
        return self.domainName
    
    def setRCode(self,rcode):
        self.rCode = rcode
        
    def getRCode(self):
        return self.rCode
    
    def setDomainSOA(self,domainSOA):
        self.domainSOA = domainSOA
        
    def getDomainSOA(self):
        return self.domainSOA
    
    def setOldRecords(self,domainRecord):
        self.oldRecords[domainRecord] = 0
    
    def getOldRecords(self,record):
        return self.oldRecords[record]
    
    def setNewRecord(self,domainRecord):
        self.newRecords[domainRecord] = 0
        
    def getNewRecord(self,record):
        return self.newRecords[record]
    
    def setRemoveRecord(self,domainRecord):
        self.removeRecords[domainRecord] = 0
        
    def getRemoveRecord(self,record):
        self.removeRecords[record]
    
    def __init__(self,domainID,domainName,timestamp):
        self.timestamp = timestamp
        self.domainName = domainName
        self.IDNName = domainName.encode("idna")
        self.domainID = domainID

        self.oldRecords = {}
        self.newRecords = {}
        self.removeRecords = {}
        
        
        