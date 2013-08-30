"""
File: DNSDomainResolver.py
Purpose
Copywrite: Sendwell 2013
"""

import dns.rdtypes.ANY
import dns.rdtypes.IN
import dns.message
import dns.zone
import dns.query
import dns.name
import dns.flags
import socket
import dns.resolver
import dns.ttl
import sys

from dns.exception import DNSException
from dns.rdataclass import *
from dns.rdatatype import *

import settings
import geoip
import DataConnect
import NamedNonBlockingResolver

class DNSDomainResolver(object):
    
    def getGEOIPCountry(self,name,code,addr):
        key = 0
        try:
            select = "SELECT geo_country_id FROM geo_country WHERE country='%s' AND code='%s'" % (name,code)
            rows = self.connect.execQuery(select)
            if len(rows) > 0:
                for row in rows:
                    key = int(row[0])
            if key == 0:
                insert = "INSERT INTO geo_country (country,code) VALUES ('%s','%s')" % (name,code)
                key = self.connect.insertQuery(insert)
                key = self.connect.getLastInsertID()
        except:
            print("GeoIP error: %s" % sys.exc_info()[0])
        return key
    
    def getGEOIPCity(self,name,code,addr,ci):
        keys = {'country' : 1, 'city' : 1}
        try:
            select = "SELECT geo_city_id FROM geo_city WHERE city='%s' AND state='%s' AND zip='%s' AND area_code='%s'" % (ci['city'],ci['region_name'],ci['postal_code'],ci['area_code'])
            rows = self.connect.execQuery(select)
            if len(rows) > 0:
                for row in rows:
                    keys['city'] = int(row[0])
            keys['country'] = self.getGEOIPCountry(name,code,addr)
            if ci['city'] != "" and ci['region_name'] != "":
                insert = "INSERT INTO geo_city (city,state,zip,area_code,geo_country_id) VALUES ('%s','%s','%s','%s',%s)" % (ci['city'],ci['region_name'],ci['postal_code'],ci['area_code'],keys['country'])
                key = self.connect.insertQuery(insert)
                keys['city'] = self.connect.getLastInsertID()
        except:
            print("GeoIP getGEOIPCity error: %s" % sys.exc_info()[0])
        return keys
    
    def recordGEOIP(self,name,code,addr):
        key = 0
        try:
            ci = self.gip.getCityByAddr(addr)
            select = "SELECT geo_coordinate_id FROM geo_coordinates WHERE latitude=%s AND longitude=%s" % (ci['latitude'],ci['longitude'])
            rows = self.connect.execQuery(select)
            if len(rows) > 0:
                for row in rows:
                    key = int(row[0])
            if key == 0: 
                keys = self.getGEOIPCity(name,code,addr,ci)
                insert = "INSERT INTO geo_coordinates (latitude,longitude,geo_city_id,geo_country_id) VALUES ('%s','%s',%s,%s)" % (ci['latitude'],ci['longitude'],keys['city'],keys['country'])
                key = self.connect.insertQuery(insert)
                key = self.connect.getLastInsertID()
        except:
            print("GeoIP error: %s" % sys.exc_info()[0])
        return key
    
    def updateSOA(self,results,soaID):
        count = 0
        try:
            for key in results:
                if key != 'expire' and key != 'ttl' and key != 'refresh' and key != 'retry' and key != 'minimum' and key != 'serial':
                    ttl = results['ttl']
                    expire = results['expire']    
                    retry = results['retry']
                    refresh = results['refresh']
                    minimum = results['minimum']
                    sql = "UPDATE soa SET ttl=%s,expire=%s,refresh=%s,retry=%s,minimum=%s WHERE soa_id=%s" % (ttl,expire,refresh,retry,minimum,soaID)
                    count = self.connect.updateQuery(sql)
                    if int(soaID) == 21 or int(soaID) == 23:
                        print "Count: %s %s" % (count,sql)
        except:
            print ("DNSDomainResolver update SOA error %s" % sys.exc_info()[0])
        return count
    
    def getDomainAddress(self,domain):
        results = []
        try:
            ### query = dns.resolver.Resolver()
            ### query.nameservers=[socket.gethostbyname(self.resolvers[self.resolverPos])]
            ### query.timeout = 2.0
            answer = self.query.query(domain,'A')
            for rdata in answer:
                results.append(rdata.address)
        except DNSException, e:
            print ("DNS error: %s %s %s" % (e.__class__,e,domain))
        return results
    
    def getDomainSerial(self,domain,dnsID):
        queryType = "SOA"
        results = {}
        try:
            ### query = dns.resolver.Resolver()
            ### query.nameservers=[socket.gethostbyname(self.resolvers[self.resolverPos])]
            ### query.timeout = 2.0
            result = self.query.query(domain,queryType)
            tmp = str(result.rrset).split(" ")
            results[domain] = self.getDomainAddress(domain)
            results['serial'] = tmp[6]
            results['refresh'] = tmp[7]
            results['retry'] = tmp[8]
            results['expire'] = tmp[9]
            results['minimum'] = tmp[10]
            results['ttl'] = result.rrset.ttl
        except DNSException as e:
            print "Error: DNSDomainResolver: %s" % (e)
        return results
        
    def getMXNameAndAddress(self,domain,dnsID):
        results = {}
        try:
            ### query = dns.resolver.Resolver()
            ### query.nameservers=[socket.gethostbyname(self.resolvers[self.resolverPos])]
            ### query.timeout = 2.0
            answer = self.query.query(domain,'MX')
            for rdata in answer:
                result = {}
                exchangeServer = rdata.exchange
                result[exchangeServer] = self.getDomainAddress(exchangeServer)
                result['expire'] = answer.expiration
                result['ttl'] = answer.rrset.ttl
                result['priority'] = rdata.preference
                results[exchangeServer] = result
        except DNSException, e:
            print ("DNS error: %s %s %s" % (e.__class__,e,domain))
        return results
    
    def recordResponse(self,results,soaID,uType,serial,timestamp):
        try:
            for key in results:
                tmp = results[key]
                addrTmp = tmp[key]
                dKey = str(key)[:-1]
                rr_id = 0
                rr_address_id = 0
                    
                sql = "SELECT * FROM rr WHERE name='%s'" % (key)
                rows = self.connect.execQuery(sql)
                if rows:
                    for row in rows:
                        rr_id = row[5]
                    sql = "UPDATE rr SET serial='%s',name='%s',priority=%s WHERE rr_id=%s" % (serial,key,tmp['priority'],soaID)
                    count = self.connect.updateQuery(sql)
                else:
                    sql = "INSERT INTO rr (soa_id,serial,name,priority,type_id) VALUES (%s,%s,'%s',%s,%s) " % (soaID,serial,key,tmp['priority'],uType)
                    count = self.connect.insertQuery(sql)
                    rr_id = self.connect.getLastInsertID()

                for aTmp in addrTmp:
                    locationName = self.gip.getCountryNameByAddr(aTmp)
                    locationCode = self.gip.getCountryCodeByName(dKey)
                    geoipKey = self.recordGEOIP(locationName, locationCode,aTmp)
                    
                    sql = "SELECT * FROM rr_address WHERE rr_address='%s'" % aTmp
                    rows = self.connect.execQuery(sql)
                    if rows:
                        for row in rows:
                            rr_address_id = row[0]
                    else:
                        sql = "INSERT INTO rr_address (rr_address,geo_coordinate_id) VALUES ('%s',%s)" % (aTmp,geoipKey)
                        count = self.connect.insertQuery(sql)
                        rr_address_id = self.connect.getLastInsertID()
                        
                    sql = "INSERT INTO rr_history VALUES (%s,%s,'%s')" % (rr_id,rr_address_id,timestamp)
                    count = self.connect.insertQuery(sql)
                    
            return count
        except:
            print ("DNSDomainResolver record response error %s" % sys.exc_info()[0])
    
    def commitTransaction(self):
        self.connect.commitTransaction()
        
    def startTransaction(self):
        self.connect.startTransaction()
        
    def rollbackTransaction(self):
        self.connect.rollbackTransaction()
    
    def endCursor(self):
        self.connect.endCursor()
    
    def adjustResolverPos(self):
        self.resolverPos += 1
        if int(self.resolverPos) >= int(self.resolverCount):
            self.resolverPos = 0
        self.query.nameservers=[socket.gethostbyname(self.resolvers[self.resolverPos])]
        self.query.timeout = 2.0
    
    def __init__(self):
        ##3 self.resolver = NamedNonBlockingResolver.NamedNonBlockingResolver()
        self.connect = DataConnect.DatabaseConnection()
        self.gip = geoip.Geoip()
        self.resolvers = settings.DBG_RESOLVERS
        self.resolvers = self.resolvers.split(" ")
        self.resolverCount = len(self.resolvers)
        self.resolverPos = 0
        self.query = dns.resolver.Resolver()
        self.adjustResolverPos()
        
        
        