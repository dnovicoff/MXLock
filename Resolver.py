"""
File: Resolver.py
Purppse: DNS resolver class. Makes all DNS calls
Copywrite: 2013 Sendwell
"""

import dns.rdtypes.ANY
import dns.rdtypes.IN
import dns.message
import dns.zone
import dns.query
import dns.name
import dns.flags
import dns.resolver
import socket
import dns.ttl

from dns.exception import DNSException
from dns.rdataclass import *
from dns.rdatatype import *

import settings

class Resolver(object):
    
    def getDomainAddress(self,domain,dnsID,source):
        queryType = 'A'
        results = []
        try:
            answer = self.resolv.query(domain,queryType)
            for rdata in answer:
                results.append(rdata.address)
            return results
        except DNSException, e:
            message = "DNS getDomainAddress: %s %s %s %s %s" % (e.__class__,e,domain,dnsID,source)
            self.log.writeLog(message)
    
    def getDomainSerial(self,domain,dnsID):
        queryType = "SOA"
        results = {}
        try:
            result = self.resolv.query(domain, queryType)
            tmp = str(result.rrset).split(" ")
            results[domain] = self.getDomainAddress(domain,dnsID,queryType)
            results['serial'] = tmp[6]
            results['refresh'] = tmp[7]
            results['retry'] = tmp[8]
            results['expire'] = tmp[9]
            results['minimum'] = tmp[10]
            results['ttl'] = result.rrset.ttl
        except dns.resolver.NXDOMAIN as e:
            message = "DNS getDomainSerial error: NXDOMAIN |%s| |%s| %s" % (e,domain,dnsID)
            self.log.writeLog(message)
        except dns.resolver.Timeout as e:
            message = "DNS getDomainSerial error: Timeout |%s| |%s| %s" % (e,domain,dnsID)
            self.log.writeLog(message)
        except DNSException as e:
            message = "DNS getDomainSerial error: Exception |%s| |%s| %s" % (e,domain,dnsID)
            self.log.writeLog(message)
        return results
    
    def getMXNameAndAddress(self,domain,dnsID):
        queryType = 'MX'
        results = {}
        try:
            answer = self.resolv.query(domain, queryType)
            for rdata in answer:
                result = {}
                exchangeServer = rdata.exchange
                result[exchangeServer] = self.getDomainAddress(exchangeServer,dnsID,queryType)
                result['expire'] = answer.expiration
                result['ttl'] = answer.rrset.ttl
                result['priority'] = rdata.preference
                results[exchangeServer] = result
        except dns.resolver.NXDOMAIN as e:
            message = "DNS getMXNameAndAddress error: NXDOMAIN %s %s %s" % (e,domain,dnsID)
            self.log.writeLog(message)
        except dns.resolver.NoAnswer as e:
            message = "DNS getMXNameAndAddress: error: MoAnswer %s %s %s" % (e,domain,dnsID)
            self.log.writeLog(message)
        except DNSException, e:
            message = ("DNS getNameAndAddress: Exception %s %s %s %s" % (e.__class__,e,domain,dnsID))
            self.log.writeLog(message)
        return results
    
    def addNameServers(self):
        for index in range(0,self.resolverCount):
            self.resolv.nameservers=[self.resolvers[index]]
            self.resolv.timeout = settings.DBG_TIMEOUT
        
    def test(self,domain):
        domain = dns.name.from_text(domain)
        nameserver = self.resolvers
        query = dns.message.make_query(domain, dns.rdatatype.ANY)
        response = dns.query.udp(query, nameserver, timeout = 2)
        print response
    
    def __init__(self,log):
        self.resolvers = settings.DBG_RESOLVERS
        self.resolv = dns.resolver.Resolver()
        self.resolvers = self.resolvers.split(" ")
        self.resolverCount = len(self.resolvers)
        self.addNameServers()
        self.log = log
        
        
        