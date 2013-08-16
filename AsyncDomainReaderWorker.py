"""
File: AsyncSomainReaderWorker
Purpose:
Copywrite: Sendwell 2013
"""

import threading
from time import sleep
import time
import string
import psycopg2
import psycopg2.extras

import MySQLdb as mdb

"""
MXLock specific classes
"""
import settings
import DomainRecord
import Domain

class AsyncDomainReaderWorker(threading.Thread):
    
    def updateDomainsTimestamp(self,timestamp,curs,ids):
        if ids.__len__() > 0:
            ids = ids.rstrip(',')
            updateQuery = "UPDATE soa SET last_check=%s WHERE soa_id IN (%s)" % (timestamp,ids)
            curs.execute(updateQuery)
            curs.connection.commit()
            
    def fetchRecords(self,domain,curs):
        sqlSelectStandardRecord = "SELECT r.rr_id,r.name,r.data,r.aux,t.data FROM rr r,type t "
        sqlSelectStandardRecord += "WHERE r.rr_id=%s AND r.type_id=t.type_id" % domain.getDomainID()
        
        curs.execute(sqlSelectStandardRecord)
        rows = curs.fetchall()
        for row in rows:
            recordID = row[0]
            name = row[1]
            data = row[2]
            aux = row[3]
            #ttl = row[3]
            uType = row[4]
            
            print "Building DomainRecord.Builder"
            domainRecord = DomainRecord(recordID).Builder().setName(name).setData(data).setAUX(aux).setTTL(ttl).setType(uType).build()
            domain.setOldRecords(domainRecord)
    
    def __init__(self):
        threading.Thread.__init__(self)
        
    def run(self):
        limit = 300
        timestamp = int(round(time.time()))
        lastDomainName = ""
        
        try:
            while True:
                conn_string = "host='%s' dbname='%s' user='%s' password='%s'" % (settings.DBG_PGSQL_SERVER,
                                                                      settings.DBG_PGSQL_DATABASE,
                                                                      settings.DBG_PGSQL_USER,
                                                                      settings.DBG_PGSQL_PASS)
                ## conn = psycopg2.connect(conn_string)
                ## conn.autocommit = True
                conn = mdb.connect(settings.DBG_PGSQL_SERVER,settings.DBG_PGSQL_USER,settings.DBG_PGSQL_PASS,settings.DBG_PGSQL_DATABASE)
                ## curs = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                        
                sqlMasterDomain = "SELECT soa_id,origin,last_check FROM soa ORDER BY last_check LIMIT "+str(limit)
                                
                ids = ""
                curs = conn.cursor()        
                curs.execute(sqlMasterDomain)
                rows = curs.fetchall()
                for row in rows:
                    domainID = row[0]
                    domainName = row[1]
                    lastCheck = row[2]
                
                    if lastCheck > (timestamp-(6*3600)):
                        continue
                
                    ids += str(domainID)+","
                    
                    domain = Domain.Domain(domainID,domainName,timestamp)
                    lastDomainName = domainName
                
                    #self.fetchRecords(domain,curs)
            
                    if ids.__len__() > 2000:
                        self.updateDomainsTimestamp(timestamp, curs, ids)
                        ids = ""
                    
                self.updateDomainsTimestamp(timestamp,curs,ids)
                ids = ""
                print ("%s" % self.__class__)
                sleep(60)
        except mdb.Error as e:
            print ("Database error %s" % e)    
            