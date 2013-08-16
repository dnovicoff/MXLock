"""
File: DNSWorker.py
Purpose:
Copywrite: Sendwell 2013
"""

import threading
import sys
from time import sleep
import random

import DomainResolver

class DNSWorder(threading.Thread):
        
    def __init__(self):
        threading.Thread.__init__(self)
        self.number = random.randint(1,1000)
        
    def run(self):
        while True:
            try:
                domainResolver = DomainResolver.DomainResolver()
                rows = domainResolver.resolveDomains()
            
                self.number += 1
                print ("%s rows updated: %s" % (self.getName(),rows))
                sleep(60)
            except:
                print ("Error: DNSWorker: %s" % sys.exc_info()[0])
            
            
            