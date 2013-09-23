"""
File: MXLock.py
Purpose: this is the domain cacheing script
Copywrite: 2013 Sendwell Inc.
"""

import sys
from argparse import ArgumentParser,ArgumentTypeError,FileType
from time import sleep

import settings
import DataConnect
import client
import DNSWorker
import logger
import DomainsReader
import DomainWhoisWorker
import MXLockClasses
import DomainsImporter
import MemcacheWriterWorker
import NamedNonBlockingResolver

def arguments():
    parser = ArgumentParser(description="MXLock Process")
    
    #This is for debugging information
    parser.add_argument("-d", "--debug", dest="debug", 
                        help="Run as debug.")
    
    #this toggles the output. More verbose the more output
    parser.add_argument("-v", "--verbosity",  action="count",  
                        help="increase output verbosity (e.g. -v -vv -vvv...)")
    
    parser.add_argument("-f", "--file", dest="file",
                        help="File name to import from (Default domains.txt)")
    
    parser.add_argument("-n", "--name", dest="name", 
                        help="List Name (Default List1")
    
    parser.add_argument("-r", "--resolver", dest="resolver", action="count", 
                        help="Run the resolver.")
    
    parser.add_argument("-m", "--memcache", dest="memcache", action="count", 
                        help="Run the memcache.")
    
    res = parser.parse_args()
    if res.verbosity is None:
        res.verbosity = 0
    if res.verbosity > 0:
        print(res)
    return res

def start(resolver, memcache):
    connect = DataConnect.DatabaseConnection()
    connect.startTransaction()
    domainQty = connect.getColumnInteger("SELECT count(*) FROM soa")
    firstRecord = connect.getColumnInteger("SELECT id FROM soa ORDER BY id ASC LIMIT 1")
    connect.endCursor()
    
    domains = DomainsReader.DomainReader()
    logName = MXLockClasses.logName()
    log = logger.logger(logName)
    
    interval = 100
    
    if (resolver):
        split = domainQty/settings.DBG_THREADS_RESOLVER
        for x in range(0,settings.DBG_THREADS_RESOLVER):
            begin = firstRecord+(x*split)
            worker = DNSWorker.DNSWorker(begin,interval,domainQty+firstRecord,firstRecord,log)
            worker.start()
            sleep(5)
            
        domainWhoisWorker = DomainWhoisWorker.DomainWhoisWorker(log)
        #domainWhoisWorker.start()
        
    if (memcache):
        split = domainQty/settings.DBG_THREADS_MEMCACHE
        for x in range(0,settings.DBG_THREADS_MEMCACHE):
            begin = firstRecord+(x*split)
            memcache = MemcacheWriterWorker.MemcacheWriterWorker(domains,begin,interval,domainQty+firstRecord,firstRecord,log)
            memcache.start()
            sleep(5)
    
    server = client.client(domains)
    #server.start()

def debug(domainName,dnsServer = None):
    try:
        resolver = NamedNonBlockingResolver.NamedNonBlockingResolver(dnsServer)
        resolver.setTimeout(settings.DBG_TIMEOUT)
        resolver.setTCP(False)
        resolver.setSingleTCPPort(False)
        
        toResolve = []
        toResolve.append(domainName)
        
        for uid in range(0,toResolve.__len__()):
            nextName = str(toResolve[uid])
            resolver.sendASync(nextName, uid) 
            
    except IOError as e:
        print ("Error: Main %s" % e) 

def importDomains(filename):
    print ("Import Domains %s" % filename)
    domainCheck = {}
    try:
        domains = []
        dFile = open(filename,'r')
        domainsImporter = DomainsImporter.DomainsImporter()
        
        lineCount = 0 
        for line in dFile:
            line = line.rstrip('\r\n')
            if line == "" or line.__len__() < 20:
                continue
            
            domain = line
            #tmpStr = line.split(',')
            #domain = tmpStr[2].split('.')
            #domain = domain[1]+"."+domain[2]
            
            if not domainCheck.has_key(domain):
                domainCheck[domain] = domain
                domains.append(domain)
            if (len(domains) > 1000):
                domainsImporter.addDomains(domains)
                domains = []
                lineCount += 1
                    
        domainsImporter.addDomains(domains)
        domains = []
        dFile.close()
    except IOError as e:
        print ("Error opening file: %s %s" % (filename,e))


if __name__ == "__main__":
    margs = arguments()
    
    exit_status = 1
    SW_DEBUG = False
    if margs.debug:
        SW_DEBUG = True
        today = "today"
        debug(margs.debug)
        
    resolver = False
    if margs.resolver:
        resolver = True
    memcache = False
    if margs.memcache:
        memcache = True
        
    if (resolver or memcache):
        #dnsModule = DNSModule.DNSModule()
        start(resolver,memcache)
    
    if margs.file is not None:
        importDomains(margs.file)
        print ("Imported Ok...")
        