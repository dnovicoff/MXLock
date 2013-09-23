"""
File: DomainsReader.py
Purpose:
Copywrite: Sendwell 2013
"""

import DomainRecord

class DomainReader(object):
    
    def domainToString(self,ID):
        domain = self.domains[ID]
        message = "Domain:\n%s" % domain.toString()
        return message

    def updateMX(self,ID,mx):
        try:
            if ID in self.domains:
                domain = self.domains[ID]
                machine = domain.getMX(mx['rrID'])
                machine.setMachine(mx['machine'])
                machine.setAddress(mx['address'])
                machine.setPriority(mx['priority'])
                machine.setType(mx['rType'])
        except KeyError as e:
            print "DomainReader updateMX: error: %s" % (e)
        
    def addMX(self,soaID,mx):
        try:
            if soaID in self.domains:
                domain = self.domains[soaID]
                domain.setMX(mx['rrID'],mx['machine'],mx['priority'],mx['address'],mx['rType'])
        except KeyError as e:
            print "DomainReader addMX: error: %s" % (e)
    
    def addDomain(self,dct):
        domain = DomainRecord.DomainRecord(dct['soaID'],dct['domain'],dct['minimum'],dct['ttl'],dct['refresh'],dct['retry'],dct['expire'])
        self.domains[dct['soaID']] = domain
        
    def updateDomain(self,dct):
        try:
            if dct['soaID'] in self.domains:
                domainRecord = self.domains[dct['soaID']]
                domainRecord.setRefresh(dct['refresh'])
                domainRecord.setRetry(dct['retry'])
                domainRecord.setExpire(dct['expire'])
                domainRecord.setMinimum(dct['minimum'])
                domainRecord.setTTL(dct['ttl'])
        except KeyError as e: 
            print "DomainReader updateDomain: error: %s" % (e)
            
    def getDomain(self,ID):
        domain = None
        try:
            if ID in self.domains:
                domain = self.domains[ID]
            return domain
        except KeyError as e:
            print "DomainReader getDomain: error: %s" % (e)
        
    def exists(self,ID):
        try:
            if ID in self.domains:
                return True
            else:
                return False
        except KeyError as e:
            print "DomainReader exists: error: %s" % (e)
            
    def mxExists(self,soaID,rrID):
        try:
            domain = self.getDomain(soaID)
            return domain.exists(rrID)
        except KeyError as e:
            print "DomainReader mxExists: error: %s" % (e)
    
    def __init__(self):
        self.domains = {}
               