"""
File: Memcache.py
Purppse: Read and write to our memcache
Copywrite: Sendwell 2013
"""

import memcache

import settings

class Memcache(object):
    
    def writeLog(self,message):
        if self.log is None:
            print "%s" % message
        else:
            self.log.writeLog(message)
    
    def readMemcache(self,key):
        results = self.mc.get('%smachines' % key)
        return results
    
    def writeMemcache(self,key,value):
        if not self.mc.set('%s:machines' % key,value,600):
            self.writeLog("Memcache error: Could not set data: %s  with key %s" % (value,key))
    
    def __init__(self,log=None):
        self.server = settings.MAILDUPE_MEMCACHED_ADDRESS
        self.port = settings.MAILDUPE_MEMCACHED_PORT
        self.mc = memcache.Client([self.server+":"+str(self.port)],debug=0)
        self.log = log
        