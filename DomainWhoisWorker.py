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
        sql ="SELECT * FROM whois_company WHERE company='%s'" % (company)
        rows = self.connect.execQuery(sql)
        if rows:
            for row in rows:
                result = row[0]
        else:
            sql = "INSERT INTO whois_company (company) VALUES ('%s')" % company
            self.connect.insertQuery(sql)
            result = self.connect.getLastInsertID()
        return result
        
    def recordAnswer(self,results,soaID):
        if results != "no match":
            try:
                tmp = results.split("\n")
                tmp[1] = tmp[1].strip()
        
                result = ""
                self.connect.startTransaction()
                sql = "SELECT * FROM whois WHERE soa_id=%s" % (soaID)
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
                print "Error: %s recordAnswer error: %s %s" % (self.threadName,sys.exc_info()[0],e)
        
    def getDomains(self):
        timestamp = MXLockClasses.getTimestamp()
        select = "SELECT soa_id,origin FROM soa WHERE last_check<%s LIMIT 1000" % (timestamp)
        self.connect.startTransaction()
        rows = self.connect.execQuery(select)
        self.connect.endCursor()
        return rows
        
    def run(self):
        while True:
            try:
                rows = self.getDomains()
                for row in rows:
                    soaID = row[0]
                    domain = row[1]
                    results = self.domainWhois.getWhois(domain)
                    results = self.domainWhois.getOwner()
                    self.recordAnswer(results,soaID)
                    sleep(600)
            except:
                print "Error: DomainWhoisWorker %s %s" % (self.threadName,sys.exc_info()[0])
    
    def __init__(self):
        threading.Thread.__init__(self)
        self.domainWhois = DomainWhois.DomainWhois()
        self.connect = DataConnect.DatabaseConnection()
        self.threadName = threading.current_thread().name
        