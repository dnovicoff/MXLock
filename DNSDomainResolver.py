"""
File: DNSDomainResolver.py
Purpose
Copywrite: Sendwell 2013
"""

import sys

import settings
import geoip
import DataConnect

class DNSDomainResolver(object):
    
    def getGEOIPCountry(self,name,code,addr):
        key = 0
        try:
            select = "SELECT id FROM geo_country WHERE vcountry='%s' AND vcode='%s'" % (name,code)
            key = self.connect.getColumnInteger(select)
            if key == 0:
                insert = "INSERT INTO geo_country (vcountry,vcode) VALUES ('%s','%s')" % (name,code)
                key = self.connect.insertQuery(insert)
                sql = "SELECT currval('geo_country_id_seq')"
                key = self.connect.getColumnInteger(sql)
        except:
            message = "GeoIP error: %s  %s %s %s" % (sys.exc_info()[0],name,code,addr)
            self.log.writeLog(message)
        return key
    
    def getGEOIPCity(self,name,code,addr,ci):
        keys = {'country' : 4, 'city' : 1}
        try:
            select = "SELECT id FROM geo_city WHERE vcity='%s' AND vstate='%s' AND vzip='%s' AND varea_code='%s'" % (ci['city'],ci['region_name'],ci['postal_code'],ci['area_code'])
            keys['city'] = self.connect.getColumnInteger(select)
            keys['country'] = self.getGEOIPCountry(name,code,addr)
            if ci['city'] != "" and ci['region_name'] != "":
                insert = "INSERT INTO geo_city (vcity,vstate,vzip,varea_code,ligeo_country_id) VALUES ('%s','%s','%s','%s',%s)" % (ci['city'],ci['region_name'],ci['postal_code'],ci['area_code'],keys['country'])
                key = self.connect.insertQuery(insert)
                sql = "SELECT currval('geo_city_id_seq')"
                keys['city'] = self.connect.getColumnInteger(sql)
        except:
            message = "GeoIP getGEOIPCity error: %s %s %s %s" % (sys.exc_info()[0],name,code,addr)
            self.log.writeLog(message)
        return keys
    
    def recordGEOIP(self,name,code,addr):
        key = 0
        try:
            ci = self.gip.getCityByAddr(addr)
            select = "SELECT id FROM geo_coordinates WHERE dlatitude=%s AND dlongitude=%s" % (ci['latitude'],ci['longitude'])
            key = self.connect.getColumnInteger(select)
            if key == 0: 
                keys = self.getGEOIPCity(name,code,addr,ci)
                insert = "INSERT INTO geo_coordinates (dlatitude,dlongitude,ligeo_city_id,ligeo_county_id) VALUES ('%s','%s',%s,%s)" % (ci['latitude'],ci['longitude'],keys['city'],keys['country'])
                key = self.connect.insertQuery(insert)
                sql = "SELECT currval('geo_coordinates_id_seq')"
                key = self.connect.getColumnInteger(sql)
        except:
            message = "recordGEOIP error: %s %s %s %s" % (sys.exc_info()[0],name,code,addr)
            self.log.writeLog(message)
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
                    sql = "UPDATE soa SET littl=%s,liexpire=%s,lirefresh=%s,liretry=%s,liminimum=%s WHERE id=%s" % (ttl,expire,refresh,retry,minimum,soaID)
                    count = self.connect.updateQuery(sql)
        except:
            message = "DNSDomainResolver update SOA error %s %s %s" % (sys.exc_info()[0],soaID,results)
            self.log.writeLog(message)
        return count
    
    def recordResponse(self,results,soaID,uType,serial,timestamp):
        count = 0
        try:
            for key in results:
                tmp = results[key]
                addrTmp = tmp[key]
                dKey = str(key)[:-1]
                rr_id = 0
                rr_address_id = 0
                    
                sql = "SELECT id FROM rr WHERE vname='%s'" % (key)
                rr_id = self.connect.getColumnInteger(sql)
                if rr_id != 0:
                    sql = "UPDATE rr SET liserial='%s',vname='%s',ipriority=%s WHERE id=%s" % (serial,key,tmp['priority'],rr_id)
                    count = self.connect.updateQuery(sql)
                else:
                    sql = "INSERT INTO rr (lisoa_id,liserial,vname,ipriority,litype_id) VALUES (%s,%s,'%s',%s,%s) " % (soaID,serial,key,tmp['priority'],uType)
                    rr_id = self.connect.insertQuery(sql)
                    sql = "SELECT currval('rr_id_seq')"
                    rr_id = self.connect.getColumnInteger(sql)

                for aTmp in addrTmp:
                    locationName = self.gip.getCountryNameByAddr(aTmp)
                    locationCode = self.gip.getCountryCodeByName(dKey)
                    geoipKey = self.recordGEOIP(locationName, locationCode,aTmp)
                    
                    sql = "SELECT id FROM rr_address WHERE vrr_address='%s'" % aTmp
                    rr_address_id = self.connect.getColumnInteger(sql)
                    if rr_address_id == 0:
                        sql = "INSERT INTO rr_address (vrr_address,ligeo_coordinate_id) VALUES ('%s',%s)" % (aTmp,geoipKey)
                        count = self.connect.insertQuery(sql)
                        sql = "SELECT currval('rr_address_id_seq')"
                        rr_address_id = self.connect.getColumnInteger(sql)

                    """
                    Column id in table rr_history is the foreign key for table rr in MySQL is was called rr_id
                    """
                    if rr_address_id != 0 and rr_id != 0:
                        sql = "INSERT INTO rr_history VALUES (%s,%s,CURRENT_TIMESTAMP)" % (rr_id,rr_address_id)
                        count = self.connect.insertQuery(sql)
        except:
            message = "DNSDomainResolver record response error %s %s %s %s %s" % (sys.exc_info()[0],soaID,uType,serial,timestamp)
            self.log.writeLog(message)
        return count
    
    def commitTransaction(self):
        self.connect.commitTransaction()
        
    def startTransaction(self):
        self.connect.startTransaction()
        
    def rollbackTransaction(self):
        self.connect.rollbackTransaction()
    
    def endCursor(self):
        self.connect.endCursor()
        
    def __init__(self,log):
        self.connect = DataConnect.DatabaseConnection()
        self.gip = geoip.Geoip()
        self.log = log
        
        
        