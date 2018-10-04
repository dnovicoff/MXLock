"""
File: MemcacheWriterMySQLWorker.py
Purpose:
Copywrite: Sendwell 2013
"""

import threading
import TimeMeasureable
from time import sleep

import DataConnect
import Memcache
import MXLockClasses


class MemcacheWriterWorker(threading.Thread):
            
    def adjustStart(self):
        self.begin += self.interval
        if int(self.begin) > self.end:
            self.begin = self.first
    
    def getDomains(self):
        sql =  "SELECT s.id,s.vorigin,s.lirefresh,s.liretry,s.liexpire,s.liminimum,s.littl,"
        sql += "r.id,r.liserial,r.vname,r.ipriority "
        sql += "FROM soa s,rr r WHERE s.id=r.lisoa_id "
        sql += "AND s.id>=%s AND s.id<%s LIMIT %s" % (self.begin,self.begin+self.interval,self.interval)
        
        #sql =  "SELECT s.id,s.vorigin,s.lirefresh,s.liretry,s.liexpire,s.liminimum,s.littl,"
        #sql += "r.id,r.liserial,r.vname,r.ipriority,"
        #sql += "rh.id,rh.lirr_address_id,count(*) AS changes,"
        #sql += "ra.id,ra.vrr_address FROM soa s "
        #sql += "INNER JOIN(SELECT id,lisoa_id,liserial,vname,ipriority FROM rr) r ON s.id=r.lisoa_id "
        #sql += "INNER JOIN(SELECT DISTINCT id,lirr_address_id,count(*) FROM rr_history GROUP BY id,lirr_address_Id ORDER BY 3 DESC) rh ON r.id=rh.id "
        #sql += "INNER JOIN(SELECT id,vrr_address FROM rr_address) ra ON rh.lirr_address_id=ra.id"
        
        self.connection.startTransaction()
        rows = self.connection.execQuery(sql)
        self.connection.endCursor()
        return rows
    
    def getDomainsMX(self,rrID):
        sql =  "SELECT rh.id,rh.lirr_address_id,rh.tstimestamp,ra.vrr_address FROM rr_history rh "
        sql += "INNER JOIN(SELECT id,vrr_address FROM rr_address) ra ON rh.lirr_address_id=ra.id "
        sql += "AND rh.id=%s ORDER BY rh.tstimestamp DESC LIMIT 1" % rrID
        
        self.connection.startTransaction()
        rows = self.connection.execQuery(sql)
        self.connection.endCursor()
        return rows
    
    def resolvMemcache(self):
        rows = self.getDomains()
        if rows:
            for row in rows:
                domainDict = {}
                domainDict['soaID'] = row[0]
                domainDict['domain'] = row[1]
                domainDict['refresh'] = row[2]
                domainDict['retry'] = row[3]
                domainDict['expire'] = row[4]
                domainDict['minimum'] = row[5]
                domainDict['ttl'] = row[6]
                     
                mx = {}
                mx['rrID'] = row[7]   
                serial = row[8]
                mx['machine'] = row[9]
                mx['priority'] = row[10]
                        
                nRows = self.getDomainsMX(mx['rrID'])
                if nRows:
                    for nRow in nRows:
                        rhID = nRow[0]
                        rhAID = nRow[1]
                        timestamp = nRow[2]
                        mx['address'] = nRow[3]
                        mx['rType'] = 5
                       
                    if self.domains.exists(domainDict['soaID']) == False:
                        self.domains.addDomain(domainDict)
                    else:
                        self.domains.updateDomain(domainDict)
                            
                    if nRows:
                        if self.domains.mxExists(domainDict['soaID'],mx['rrID']) == False:
                            self.domains.addMX(domainDict['soaID'],mx)
                        else:
                            self.domains.updateMX(domainDict['soaID'],mx)
                        mData = (mx['priority'],mx['address'])
                        self.mc.writeMemcache(mx['machine'], mData)
    
    def run(self):
        try:
            while True:
                self.resolvMemcache()
                sleep(60)        
                self.adjustStart()                               
        except Exception as e:
            message = "MemcacheWriterWorker Error: %s" % e
            MXLockClasses.writeLog(message,self.log)
         
    def __init__(self,domains,begin,interval,end,firstRecord,log=None):
        threading.Thread.__init__(self)
        self.threadName = self.getName()
        self.domains = domains
        self.begin = begin
        self.interval = interval
        self.end = end+10
        self.first = firstRecord
        self.connection = DataConnect.DatabaseConnection()
        self.log = log
        self.mc = Memcache.Memcache(self.log)
        
        
        