"""
File: DomainResolver.py
Purpose:
Copywrite: Sendwell 2013
"""
import time
import sys

import Domain
import DomainsReader
import DataConnect
from DNSDomainResolver import DNSDomainResolver

class DomainResolver():
    
    def resolveDomains(self):
        timestamp = int(round(time.time()))
        timeForQuery = timestamp-(360)
        self.resolveDomains = []

        """ Move to DNSDomainResolver """        
        select = "SELECT * FROM rtype"
        self.connection.startTransaction()
        results = self.connection.execQuery(select)
        types = {}
        for result in results:
            types[result[1]] = result[0]
        self.connection.endCursor()
        domainResolver = DNSDomainResolver()
        
        """ Move this to DNSDomainResolver """
        select = "SELECT * FROM soa WHERE last_check < %s LIMIT 100" % timeForQuery
        self.connection.startTransaction()
        rows = self.connection.execQuery(select)
        self.connection.endCursor()

        ids = ""
        for row in rows:
            try:
                soaID = row[0]
                ids += str(row[0])+","
                domain = row[1]
                print("Working with domain: %s" % domain)
                serial = domainResolver.getDomainSerial(domain, soaID) 
                if serial['serial'] != "":
                    domainResolver.startTransaction()
                    success = domainResolver.setDomainSerial(serial['serial'], soaID)
                    if success > 0:
                        success = domainResolver.updateSOA(serial,soaID)
                        if success > 0:
                            results = domainResolver.getMXNameAndAddress(domain, soaID)
                            domainResolver.recordResponse(results,soaID,types['MX'],serial['serial'])
                            domainResolver.commitTransaction()
                        else:
                            domainResolver.rollbackTransaction()
                    else:
                        domainResolver.rollbackTransaction()
            except:
                print("Error: DomainResolver: %s" % sys.exc_info()[0])

        rowsAffected = 0
        if (ids != ""):                
            ids = ids[:-1]
            self.connection.startTransaction()
            update = "UPDATE soa SET last_check=%s WHERE soa_id IN (%s)" % (timestamp,ids)
            rowsAffected = self.connection.updateQuery(update)
            self.connection.commitTransaction()
        
        return rowsAffected
            
    def __init__(self):
        self.connection = DataConnect.DatabaseConnection()
        
        
         