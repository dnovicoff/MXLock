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
    
    def selectRRHistory(self,rrID):
        rows = None
        try:
            sql =  "SELECT * FROM rr_history rh,rr_address ra WHERE rh.id=%s " % rrID
            sql += "AND rh.lirr_address_id=ra.id ORDER BY rh.tstimestamp DESC,ra.id DESC"
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
                            mean = {}
                            tme = {}
                            lastEpoch = 0
                            lastRAID = 0
                            moved = 0
                            for row in rows:
                                raID = int(row[3])
                                sinceEpoch = MXLockClasses.convertToEpoch(row[2])
                                if not raID == lastRAID and not lastEpoch == sinceEpoch and not lastEpoch == 0:
                                    if not tme.has_key(raID):
                                        moved += 1 
                                if tme.has_key(raID):
                                    if mean.has_key(raID):
                                        mean[raID] += tme[raID] - sinceEpoch
                                    else:
                                        mean[raID] = tme[raID] - sinceEpoch
                                    
                                tme[raID] = sinceEpoch
                                lastEpoch = sinceEpoch
                                lastRAID = raID
                                print "RRID: %s   Seconds: %s  Address %s  AddressID %s" % (rrID,sinceEpoch,row[5],row[3])
                            
                            for key in mean:
                                mean[key] = mean[key] / mean.__len__()
                                print "          Mean time: %s Interval count %s  movement: %s" % (mean[key],tme.__len__(),moved)
                
                self.curPos += 1
                if self.curPos >= self.domains.getLength():
                    self.curPos = 0
                    
                sleep(1)
            except IOError as e:
                MXLockClasses.writeLog("Statistics error: %s" % e,self.log)
            except KeyError as e:
                MXLockClasses.writeLog("Statistics error keyerror: %s" % e, self.log)
    
    def __init__(self,domains,log=None):
        threading.Thread.__init__(self)
        self.threadName = threading.current_thread().name
        self.domains = domains
        self.log = log
        self.connect = DataConnect.DatabaseConnection()
        self.curPos = 0
        
        