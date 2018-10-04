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
import MXLockClasses
import DomainResolver
import MemcacheWriterWorker

class client(threading.Thread):

    def writeDomains(self,domain):
        ID = domain[0]
        tmp = {}
        tmp['soaID'] = ID
        tmp['domain'] = domain[1]
        tmp['refresh'] = domain[2]
        tmp['retry'] = domain[3]
        tmp['expire'] = domain[4]
        tmp['minimum'] = domain[5]
        tmp['ttl'] = domain[6]
        self.domains.addDomain(tmp)
        return self.domains.domainToString(ID)

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
        sql = "SELECT vorigin FROM soa WHERE vorigin LIKE '%s'" % (term)
        self.connect.startTransaction()
        rows = self.connect.execQuery(sql)
        self.connect.commitTransaction()
        if rows:
            for row in rows:
                for x in range (0,len(row)):
                    results += row[x]
                results += "\n"
        if results.__len__() <= 0:
            results = "Could not find domains with search term, %s\n" % term
        return results
    
    def findDomains(self,term):
        term = term[:-1]
        message = ""
        sql = "SELECT * FROM soa WHERE vorigin = '%s'" % (term)
        self.connect.startTransaction()
        rows = self.connect.execQuery(sql)
        self.connect.commitTransaction()
        if rows:
            for row in rows:
                message = self.writeDomains(row)
        return message
    
    def showTables(self):
        results = ""
        sql = "\d"
        self.connect.startTransaction()
        rows = self.connect.execQuery(sql)
        if rows:
            for row in rows:
                results += row[0]+"\n"
        self.connect.commitTransaction()
        return results
    
    def resolvDomain(self,domain):
        domain = domain[:-1]
        rows = None
        if domain.__len__() > 1:
            sql = "SELECT * FROM soa WHERE vorigin='%s'" % domain
            self.connect.startTransaction()
            rows = self.connect.execQuery(sql)
            self.connect.endCursor()
            uid = 0
            if rows:
                for row in rows:
                    uid = row[0] 
            domainResolver = DomainResolver.DomainResolver(uid,0,self.log,self.threadName,0,1)
            success = domainResolver.resolveDomains(self.types,self.keys)
            if success > 0:
                message = self.writeDomains(row)
                memcache = MemcacheWriterWorker.MemcacheWriterWorker(self.domains,uid,1,0,0,self.log)
                memcache.resolvMemcache()
        return message
    
    def setRegEx(self):
        self.regEx['showtables'] = re.compile("^Show Tables")
        self.regEx['like'] = re.compile("^like (.*)\\n")
        self.regEx['find'] = re.compile("^find (.*)\\n")
        self.regEx['exec'] = re.compile("^exec (.*)\\n")
        self.regEx['resolve'] = re.compile("^resolve (.*)\\n")
    
    def listening(self):
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind((self.host,self.port))
            self.server.listen(5)
        except socket.error as e:
            MXLockClasses.writeLog("Error server socket error: %s %s" % (sys.exc_info()[0],e),self.log)
    
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
                elif self.regEx['like'].match(data):
                    match = self.regEx['like'].match(data)
                    results = self.searchDomains(match.group(1))
                elif self.regEx['find'].match(data):
                    match = self.regEx['find'].match(data)
                    results = self.findDomains(match.group(1))
                elif self.regEx['exec'].match(data):
                    match = self.regEx['exec'].match(data)
                    results = self.execSQL(match.group(1))
                elif self.regEx['resolve'].match(data):
                    match = self.regEx['resolve'].match(data)
                    results = self.resolvDomain(match.group(1))
                conn.send(results)
            except socket.error as e:
                MXLockClasses.writeLog("DNS Client socket error: %s" % e,self.log)
            except TypeError as e:
                MXLockClasses.writeLog("DNS Client type error: %s" % e,self.log)
            except IndexError as e:
                MXLockClasses.writeLog("DNS client index error: %s" % (sys.exc_info()[0]),self.log)
            except:
                MXLockClasses.writeLog("DNS client error",self.log)
            finally:
                conn.close()
    
    def __init__(self,domains,log=None,keys=None):
        threading.Thread.__init__(self)
        self.threadName = threading.current_thread().name
        self.domains = domains
        self.connect = DataConnect.DatabaseConnection()
        self.host = socket.gethostname()
        self.log = log
        self.port = 60000
        self.regEx = {}
        self.setRegEx()
        self.listening()
        self.keys = keys
        self.types = MXLockClasses.createTypes()
        
        
        