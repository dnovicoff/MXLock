"""
File: AtomicInteger.py
Purpose: an integer value that may change it's value atomically
CopyWrite: Sendwell 2013
"""

import os
import sys
import threading

class AtomicInteger(object):
    
    def increase(self,inc = 1):
        self.lock.acquire()
        self.counter = self.counter + inc
        self.lock.release()
        return
    
    def decrease(self,inc = 1):
        self.lock.acquire()
        self.counter = self.counter - inc
        self.lock.release()
        return
    
    def get(self):
        return self.counter
    
    def __init__(self,integer = 0):
        self.counter = integer
        self.lock = threading.RLock()
        return