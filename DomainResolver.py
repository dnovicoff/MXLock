"""
File: DomainResolver.py
Purpose:
Copywrite: Sendwell 2013
"""
import sys
import string

import Resolver
import MXLockClasses
import DataConnect
from DNSDomainResolver import DNSDomainResolver

class DomainResolver():
    
    def getDomain(self,domain):
        result = ""
        tmp = domain.split(".")
        for index in range(1,len(tmp)):
            result += tmp[index]+"."
        return result[:-1]
    
    def arrayLength(self,array):
        success = 1
        if len(array) < 1:
            success = 0
        return success
    
    def resolveDomains(self):
        timestamp = MXLockClasses.getTimestamp()
        timeForQuery = timestamp-(3600*15)
        self.resolveDomains = []

        """ Move to DNSDomainResolver """        
        select = "SELECT * FROM rtype"
        self.connection.startTransaction()
        results = self.connection.execQuery(select)
        types = {}
        for result in results:
            types[result[1]] = result[0]
        self.connection.endCursor()
        domainResolver = DNSDomainResolver(self.log)
        
        """ Move this to DNSDomainResolver """
        select =  "SELECT id,vorigin FROM soa WHERE lilast_check < {0} AND id>= {1} AND id<= {2} LIMIT {3}".format(timeForQuery,self.begin,self.begin+self.interval,self.interval)
        self.connection.startTransaction()
        rows = self.connection.execQuery(select)
        self.connection.endCursor()
        ids = ""
        if rows:
            for row in rows:
                ids += str(row[0])+","
            
        rowsAffected = 0
        if (ids != ""):                
            ids = ids[:-1]
            self.connection.startTransaction()
            update = "UPDATE soa SET lilast_check=%s WHERE id IN (%s)" % (timestamp,ids)
            self.connection.updateQuery(update)
            self.connection.commitTransaction()

        if rows:
            for row in rows:
                try:
                    soaID = row[0]
                    domain = row[1]
                
                    """ Try twice to make sure we have the domain and not a machine name """
                    serial = self.resolver.getDomainSerial(domain, soaID)
                    if len(serial) < 1:
                        serial['serial'] = 0
                    ##if self.arrayLength(serial) < 1:
                    ##    serial = self.resolver.getDomainSerial(self.getDomain(domain),soaID)
                    """ 
                        It has been found that some records will not have an SOA record but have
                        an MX host record. Look for those.
                    """
                
                    if len(serial) > 0:
                        domainResolver.startTransaction()
                        success = domainResolver.updateSOA(serial,soaID)
                        domainResolver.endCursor()
                
                    domainResolver.startTransaction()    
                    results = self.resolver.getMXNameAndAddress(domain, soaID)
                    if len(results) > 0:
                        success = domainResolver.recordResponse(results,soaID,types['MX'],serial['serial'],timeForQuery)
                        if success > 0:
                            domainResolver.commitTransaction()
                            rowsAffected += 1
                        else:
                            domainResolver.rollbackTransaction()
                    else:
                        domainResolver.rollbackTransaction()
                    domainResolver.endCursor()
                except:
                    message = "DomainResolver error: check dns.rcode.SERVFAIL %s %s" % (sys.exc_info()[0],self.name)
                    self.log.writeLog(message)
        
        return rowsAffected
            
    def __init__(self,begin,interval,log,name):
        self.resolver = Resolver.Resolver(log)
        self.connection = DataConnect.DatabaseConnection()
        self.begin = begin
        self.interval = interval
        self.log = log
        self.name = name
        
        