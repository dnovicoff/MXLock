"""
File: Statistics.py
Purpose: Gleem information from rr_history
Copywrite: Sendwell 2013
"""

import threading
from time import sleep

import DataConnect
import MXLockClasses

class Statistics(threading.Thread):
    
    def findMean(self,count,tme):
        second = 0
        diff = 0
        for key in tme:
            first = tme[key]
            if second != 0:
                diff += first-second
            second = first
        mean = diff / count
        return mean
    
    def selectRRHistory(self,rrID):
        rows = None
        try:
            sql =  "SELECT * FROM rr_history rh,rr_address ra WHERE rh.id=%s " % rrID
            sql += "AND rh.lirr_address_id=ra.id"
            self.connect.startTransaction()
            rows = self.connect.execQuery(sql)
            self.connect.endCursor()
        except RuntimeError as e:
            MXLockClasses.writeLog("DNS Statistics error: %s" % e,self.log)
        return rows
    
    def run(self):
        while True:
            try:
                domainCount = self.domains.getLength()
                soaID = self.domains.getNextDomainID()
                if soaID is not None:
                    mxCount = self.domains.getMXLength(soaID)
                    for x in range(0,mxCount):
                        rrID = self.domains.getNextDomainMXID(soaID)
                        rows = self.selectRRHistory(rrID) 
                        if rows:
                            record = 0
                            tme = {}
                            addr = {}
                            for row in rows:
                                sinceEpoch = MXLockClasses.convertToEpoch(row[2])
                                tme[record] = sinceEpoch
                                addr[record] = row[5]
                                record += 1
                                print "RRID: %s   Seconds: %s  Row: %s" % (rrID,sinceEpoch,row)
                            
                            mean = self.findMean(record,tme)
                            print "Mean time: %s" % mean
                
                self.curPos += 1
                if self.curPos >= self.domains.getLength():
                    self.curPos = 0
                    
                sleep(1)
            except IOError as e:
                MXLockClasses.writeLog("Statistics error: %s" % e,self.log)
    
    def __init__(self,domains,log=None):
        threading.Thread.__init__(self)
        self.threadName = threading.current_thread().name
        self.domains = domains
        self.log = log
        self.connect = DataConnect.DatabaseConnection()
        self.curPos = 0