"""
File: DNSModule.py
Purpose:
Copywrite: Sendwell 2013
"""

import pygeoip
import settings
import NamedNonBlockingResolver
import DNSDomainResolver

class DNSModule(object):
    
    def getLookupService(self,config):
        GEODir = settings.DBG_GEODIR
        
    def getIPToCountry(self):
        GEODir = settings.DBG_GEODIR
       
    def getMemcacheClient(self):
        address = []
         
    def getDomainsWriter(self):
        writerNode = settings.DBG_WRITER
        
        if "async" == writerNode:
            self.voidDomainsWriter = 0
            return self.voidDomainsWriter
        if "void" == writerNode:
            self.MemcacheDomainsWriter = 0
            return self.MemcacheDomainsWriter
            
        self.StandardDomainWriter = 0
        return self.StandardDomainWriter
    
    def getDomainsReader(self):
        readerMode = settings.DBG_READER
        
        if "async" == readerMode:
            self.AsyncDomainsReader = 0
            return self.AsyncDomainsReader
        
        self.StandardDomainsReader = 0
        return self.StandardDomainsReader
    
    def getDomainResolver(self):
        resolverHosts = settings.DBG_RESOLVERS
        if resolverHosts != "" and resolverHosts == "fake":
            self.fakeDomainResolver = 0
            return self.fakeDomainResolver
        
        self.dnsDomainResolver = 0
        return self.dnsDomainResolver
    
    def getResolvers(self):
        resolvers = []
        
        resolverHosts = settings.DBG_RESOLVERS
        if (resolverHosts != "" and resolverHosts == "fake"):
            self.fakeDomainResolver = 0
            return self.fakeDomainResolver
        
        timeout = 1
        timeoutConfig = settings.DBG_TIMEOUT
        if timeoutConfig != "":
            timeout = int(timeoutConfig)
            
        tcp = True
        UDPConfig = settings.DBG_UDP
        if UDPConfig != "" and UDPConfig == True:
            tcp = False
            
        singlePort = False
        singlePortConfig = settings.DBG_SINGLEPORT
        if singlePortConfig != "" and singlePortConfig == True:
            singlePort = True
            
        while resolvers.__len__() < 16:
            if resolverHosts != "" and resolverHosts.__len__() != 0:
                hosts = resolverHosts.split()
                for host in hosts:
                    if host.__len__() == 0 or host == "":
                        continue
                    try:
                        resolver = NamedNonBlockingResolver(host)
                        resolver.SetTimeout(timeout)
                        resolver.setTCP(tcp)
                        resolver.setSingleTCPPort(singlePort)
                        dnsDomainResolver = DNSDomainResolver.DNSDomainResolver()
                        dnsDomainResolver.setNamedNonBlockingResolver(resolver)
                        resolvers.append(resolver)
                    except IOError as e:
                        print ("Error: DNSModule  %s" % e)
            else:
                try:
                    resolver = NamedNonBlockingResolver(host)
                    resolver.SetTimeout(timeout)
                    resolver.setTCP(tcp)
                    resolver.setSingleTCPPort(singlePort)
                    dnsDomainResolver = DNSDomainResolver.DNSDomainResolver()
                    dnsDomainResolver.setNamedNonBlockingResolver(resolver)
                    resolvers.append(resolver)
                except IOError as e:
                    print ("Error: DNSModule %s" % e)
    
        return resolvers
    
    