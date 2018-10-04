"""
File: domainWhois.py
Purpose: determine who owns an IP address
Copywrite: Sendwell 2013
"""

import threading
from time import sleep
import sys

import DomainWhois
import DataConnect
import MXLockClasses

class DomainWhoisWorker(threading.Thread):
        
    def getWhoisCompanyID(self,company):
        company = company.strip()
        result = 0
        sql ="SELECT * FROM whois_company WHERE vcompany='%s'" % (company)
        rows = self.connect.execQuery(sql)
        if rows:
            for row in rows:
                result = row[0]
        else:
            sql = "INSERT INTO whois_company (vcompany) VALUES ('%s')" % company
            self.connect.insertQuery(sql)
            sql = "SELECT currval('whois_company_id_seq')"
            rows = self.connect.execQuery(sql)
            if rows:
                for row in rows:
                    result = row[0]
        return result
        
    def recordAnswer(self,results,soaID):
        if results != "no match":
            try:
                tmp = results.split("\n")
                tmp[1] = tmp[1].strip()
        
                result = ""
                self.connect.startTransaction()
                sql = "SELECT * FROM whois WHERE id=%s" % (soaID)
                rows = self.connect.execQuery(sql)
                if rows:
                    for row in rows:
                        result = row[1]
                if result == "":
                    whoisCompanyID = self.getWhoisCompanyID(tmp[0])
                    sql = "INSERT INTO whois VALUES (%s,%s,'%s')" % (soaID,whoisCompanyID,tmp[1])
                    self.connect.insertQuery(sql)
                self.connect.commitTransaction()
            except IndexError as e:
                message =  "DomainWhoisWorker recordAnswer error: %s %s %s" % (self.threadName,sys.exc_info()[0],e)
                self.log.writeLog(message)
        else:
            self.log.writeLog(self.domainWhois.lastRecord)
        
    def getDomains(self):
        timestamp = MXLockClasses.getTimestamp()
        select = "SELECT id,vorigin FROM soa WHERE id not in (SELECT id FROM whois) LIMIT 1000"
        self.connect.startTransaction()
        rows = self.connect.execQuery(select)
        self.connect.endCursor()
        return rows
        
    def run(self):
        while True:
            #try:
                rows = self.getDomains()
                if rows:
                    for row in rows:
                        soaID = row[0]
                        domain = row[1]
                        results = self.domainWhois.getWhois(domain)
                        if results:
                            results = self.domainWhois.getOwner()
                            self.recordAnswer(results,soaID)
                        sleep(60)
                else:
                    print "No matching records"
            #except:
            #    message = "DomainWhoisWorker error: %s %s" % (self.threadName,sys.exc_info()[0])
            #    self.log.writeLog(message)
    
    def __init__(self,log):
        threading.Thread.__init__(self)
        self.domainWhois = DomainWhois.DomainWhois()
        self.connect = DataConnect.DatabaseConnection(log)
        self.threadName = threading.current_thread().name
        self.log = log
        