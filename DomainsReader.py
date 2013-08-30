"""
File: DomainsReader.py
Purpose:
Copywrite: Sendwell 2013
"""

import DomainRecord

class DomainReader(object):
    
    def domainToString(self,ID):
        domain = self.domains[ID]
        print "Domain:\n"+domain.toString()
    
    def addDomain(self,ID,domain):
        self.domains[ID] = domain
        
    def findDomain(self,ID):
        domain = ""
        for domains in self.domains:
            if domains == ID:
                domain = self.domains[domains]
        return domain
    
    def __init__(self):
        self.domains = {}
        
        