"""
File: client.py
Purpose: Open a socket and let a client connect
Copywrite: Sendwell 2013
"""

import threading
import socket
import sys
import re

import DataConnect
import DomainRecord
import DomainsReader

class client(threading.Thread):

    def writeDomains(self,domain):
        ID = domain[0]
        origin = str(domain[1])
        minimum = domain[2]
        TTL = domain[3]
        refresh = domain[4]
        retry = domain[5]
        expire = domain[6]
        lastcheck = domain[7]
        locked = domain[8]
        domain = DomainRecord.DomainRecord(ID,origin,minimum,TTL,refresh,retry,expire,lastcheck,locked)
        self.domains.addDomain(ID,domain)
        self.domains.domainToString(ID)

    def readDomains(self,domain,ID):
        domain = self.domains[ID]
        return domain.toString()

    def execSQL(self,sql):
        results = ""
        sql = sql[:-1]
        self.connect.startTransaction()
        rows = self.connect.execQuery(sql)
        self.connect.commitTransaction()
        if rows:
            for row in rows:
                for x in range (0,len(row)):
                    results += str(row[x])+" "
                results += "\n"
        return results
            
    def searchDomains(self,term):
        term = term[:-1]
        term = '%'+term+'%'
        results = ""
        sql = "SELECT origin FROM soa WHERE origin LIKE '%s'" % (term)
        self.connect.startTransaction()
        rows = self.connect.execQuery(sql)
        self.connect.commitTransaction()
        if rows:
            for row in rows:
                self.writeDomains(row)
                for x in range (0,len(row)):
                    results += row[x]+" "
                results += "\n"
        if results.__len__() <= 0:
            results = "Could not find domains with search term, %s\n" % term
        return results
    
    def findDomains(self,term):
        term = term[:-1]
        results = ""
        sql = "SELECT * FROM soa WHERE origin = '%s'" % (term)
        self.connect.startTransaction()
        rows = self.connect.execQuery(sql)
        self.connect.commitTransaction()
        if rows:
            for row in rows:
                self.writeDomains(row)
                for x in range(0,len(row)):
                    results += str(row[x])+" "
                results += "\n"
        return results
    
    def showTables(self):
        results = ""
        sql = "SHOW TABLES"
        self.connect.startTransaction()
        rows = self.connect.execQuery(sql)
        if rows:
            for row in rows:
                results += row[0]+"\n"
        self.connect.commitTransaction()
        return results
    
    def setRegEx(self):
        self.regEx['showtables'] = re.compile("^Show Tables")
        self.regEx['like'] = re.compile("^like (.*)\\n")
        self.regEx['find'] = re.compile("^find (.*)\\n")
        self.regEx['exec'] = re.compile("^exec (.*)\\n")
    
    def listening(self):
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind((self.host,self.port))
            self.server.listen(5)
        except socket.error as e:
            print "Error server socket error: %s %s" (sys.exc_info()[0],e)
    
    def close(self):
        self.server.close()
            
    def run(self):
        while 1:
            try:
                conn,address = self.server.accept()

                results = ""
                data = conn.recv(1024)
                if not data: 
                    break
                
                if self.regEx['showtables'].match(data):
                    results = self.showTables()
                if self.regEx['like'].match(data):
                    match = self.regEx['like'].match(data)
                    results = self.searchDomains(match.group(1))
                if self.regEx['find'].match(data):
                    match = self.regEx['find'].match(data)
                    results = self.findDomains(match.group(1))
                if self.regEx['exec'].match(data):
                    match = self.regEx['exec'].match(data)
                    results = self.execSQL(match.group(1))
                conn.send(results)
            except socket.error as e:
                print "Failed to create socket %s" % e
            except:
                print "Error: client thread runnable: %s" % (sys.exc_info()[0])
            finally:
                conn.close()
    
    def __init__(self,domains):
        threading.Thread.__init__(self)
        self.threadName = threading.current_thread().name
        self.domains = domains
        self.connect = DataConnect.DatabaseConnection()
        self.host = socket.gethostname()
        self.port = 60000
        self.regEx = {}
        self.setRegEx()
        self.listening()
        
        
        