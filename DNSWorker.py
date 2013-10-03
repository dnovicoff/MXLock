"""
File: DNSWorker.py
Purpose:
Copywrite: Sendwell 2013
"""

import threading
import sys
from time import sleep

import DomainResolver
import MXLockClasses

class DNSWorker(threading.Thread):
        
    def __init__(self,begin,interval,end,firstRecord,log=None):
        threading.Thread.__init__(self)
        self.threadName = self.getName()
        self.begin = begin
        self.interval = interval
        self.end = end+10
        self.first = firstRecord
        self.number = MXLockClasses.getRandomNumber(0,1000)
        self.log = log
        
    def adjustStart(self):
        self.begin += self.interval
        if int(self.begin) > int(self.end):
            self.begin = self.first
        
    def run(self):
        while True:
            try:
                domainResolver = DomainResolver.DomainResolver(self.begin,self.interval,self.log,self.threadName)
                rows = domainResolver.resolveDomains()
            
                self.number += 1
                message = "%s rows updated: %s" % (self.threadName,rows)
                ## self.log.writeLog(message)
                print "DNSWorder: %s" % message
                self.adjustStart()
                sleep(60)
            except:
                self.log.writeLog("Error: DNSWorker: %s" % sys.exc_info()[0])
                
                
                