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
        
    def __init__(self,begin,interval,end):
        threading.Thread.__init__(self)
        self.threadName = threading.current_thread().name
        self.begin = begin
        self.interval = interval
        self.end = end
        self.number = MXLockClasses.getRandomNumber(0,1000)
        
    def adjustStart(self):
        self.begin += self.interval
        if int(self.begin) > int(self.end):
            self.begin = 0
        
    def run(self):
        while True:
            try:
                domainResolver = DomainResolver.DomainResolver(self.begin,self.interval)
                rows = domainResolver.resolveDomains()
            
                self.number += 1
                print ("%s rows updated: %s" % (self.threadName,rows))
                self.adjustStart()
                sleep(60)
            except:
                print ("Error: DNSWorker: %s" % sys.exc_info()[0])
            
            
            