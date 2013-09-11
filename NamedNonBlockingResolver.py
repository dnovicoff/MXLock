"""
File: NamedNonBlockingResolver.py
Purpose:
Copywrite: Sendwell 2013
"""

import dns.message
import dns.query
import dns.name
import dns.flags

import settings

class NamedNonBlockingResolver(object):
    
    def sendASync(self,name,uid):
        ADDITIONAL_RDCLASS = 65535
        name = dns.name.from_text(name, dns.name.root)
        request = dns.message.make_query(name, dns.rdatatype.ANY)
        request.flags |= dns.flags.AD
        request.find_rrset(request.additional,dns.name.root,ADDITIONAL_RDCLASS,dns.rdatatype.OPT,create=True,force_unique=True)
        response = dns.query.udp(request,self.resolvers[self.resolverPos])
        if response:
            response.id = uid
            print ("Answer %s" % response.answer)
            print ("Additional %s" % response.additional)
            print ("Authority: %s" % response.authority)
            print ("Payload %s" % response.payload)
            print ("Other data %s" % response.other_data)
            print ("To text %s" % response.to_text())
        else:
            self.adjustResolverPos()
            self.sendASync(name,uid)
    
    def setTimeout(self,timeout):
        self.timeout = timeout
        
    def setTCP(self,tcp):
        self.TCP = tcp
        
    def setSingleTCPPort(self,singlePort):
        self.singlePort = singlePort
        
    def getDNSServer(self):
        return self.DNSServer
    
    def adjustResolverPos(self):
        self.resolverPos += 1
        if int(self.resolverPos) >= int(self.resolverCount):
            self.resolverPos = 0
    
    def __init__(self,dnsServer=None):
        if dnsServer is not None:
            self.DNSServer = dnsServer
        else:
            self.DNSServer = "Default DNS Server"
        self.resolvers = settings.DBG_RESOLVERS
        self.resolvers = self.resolvers.split(" ")
        self.resolverCount = len(self.resolvers)
        self.resolverPos = 0
        self.query = dns.resolver.Resolver()
            
            
            