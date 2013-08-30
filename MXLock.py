"""
File: MXLock.py
Purpose: this is the domain cacheing script
Copywrite: 2013 Sendwell Inc.
"""

import sys
import string
from argparse import ArgumentParser,ArgumentTypeError,FileType

import settings
import client
import DNSWorker
import DomainWhoisWorker
import DNSModule
import DomainsReader
import DomainsImporter
import MemcacheWriterMySQLWorker
import NamedNonBlockingResolver

def arguments():
    parser = ArgumentParser(description="MXLock Process")
    
    #This is for debugging information
    parser.add_argument("-d", "--debug", dest="debug", 
                        help="Run as debug.")
    
    #this toggles the output. More verbose the more output
    parser.add_argument("-v", "--verbosity",  action="count",  
                        help="increase output verbosity (e.g. -v -vv -vvv...)")
    
    parser.add_argument("-f", "--file", dest="file", default="domains.csv",
                        help="File name to import from (Default domains.csv)")
    
    parser.add_argument("-n", "--name", dest="name", default="List1", 
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
    domains = DomainsReader.DomainReader()
    
    if (resolver):
        interval = 100
        domainQty = 100
        #if (settings.DBG_READER == "async"):
        #    asyncDomainWorker = AsyncDomainReaderWorker.AsyncDomainReaderWorker()
        #    asyncDomainWorker.start()
                             
        for x in range(0,settings.DBG_THREADS_RESOLVER):
            split = domainQty/settings.DBG_THREADS_RESOLVER
            begin = split*x
            worker = DNSWorker.DNSWorker(begin,interval,domainQty)
            worker.start()
            
        domainWhoisWorker = DomainWhoisWorker.DomainWhoisWorker()
        domainWhoisWorker.start()
        server = client.client(domains)
        ### server.start()
        
    if (memcache):
        for x in range(0,settings.DBG_THREADS_MEMCACHE):
            ### Turn on the memcache stuff
            x = x + 1

def debug(domainName,dnsServer = None):
    try:
        resolver = NamedNonBlockingResolver.NamedNonBlockingResolver(dnsServer)
        resolver.setTimeout(3)
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
            
            tmpStr = line.split(',')
            domain = tmpStr[2].split('.')
            domain = domain[1]+"."+domain[2]
            
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
    
    if SW_DEBUG:
        sqlHost = settings.DBG_PGSQL_SERVER
        sqlUser = settings.DBG_PGSQL_USER
        sqlPass = settings.DBG_PGSQL_PASS
        sqlDB = settings.DBG_PGSQL_DATABASE
        sqlPort = settings.DBG_PGSQL_PORT
        
    if SW_DEBUG:
        print sqlHost
        print sqlUser
        print sqlPass
        print sqlDB
    
    if margs.debug:
        today = "today"
        #debug(margs.debug)
        
    resolver = False
    if margs.resolver:
        resolver = True
    memcache = False
    if margs.memcache:
        memcache = True
        
    if (resolver or memcache):
        #dnsModule = DNSModule.DNSModule()
        start(resolver,memcache)
    
    if margs.file != "":
        work = 1
        # importDomains(margs.file)
        print ("Imported Ok...")
        