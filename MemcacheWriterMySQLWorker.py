"""
File: MemcacheWriterMySQLWorker.py
Purpose:
Copywrite: Sendwell 2013
"""

import threading
import TimeMeasureable

class MemcacheWriterMySQLWorker(threading.Thread):
    
    def run(self):
        limit = 100
        maxIter = 1000 / self.SLEEP
        try:
            while True:
                iterCnt = 0
                domains = []
                
                while (iterCnt < maxIter and len(domains) < limit):
                    iterCnt += 1
                    domains.append(domain)
                                     
        except Exception as e:
            print("Error: %s" % e)
         
    def __init__(self):
        self.SLEEP = 50
        