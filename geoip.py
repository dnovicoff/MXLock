"""
File: geoip.py
PUrpose: Associate a location to IP address
Copywrite: Sendwell 2013
"""

import pygeoip
import sys

import settings

class Geoip(object):
    
    def getASNByName(self,name):
        name = self.gi4.org_by_name(name)
        return name
    
    def getISPByName(self,name):
        name = self.gi4.org_by_name(name)
        return name
    
    def getOrganizationByName(self,name):
        name = self.gi4.org_by_name(name)
        return name
    
    def getCityByAddr(self,addr):
        record = self.giCity4.record_by_addr(addr)
        return record
    
    def getRegionByName(self,name):
        region = self.gi4.region_by_name(name)
        return region
    
    def getCountryNameByAddr(self,addr):
        name = self.gi4.country_name_by_addr(addr)
        return name
    
    def getCountryCodeByAddr(self,addr):
        code = self.gi4.country_code_by_addr(addr)
        return code
    
    def getCountryCodeByName(self,name):
        code = self.gi4.country_code_by_name(name)
        return code
    
    def __init__(self):
        self.gi4 = pygeoip.GeoIP(settings.DBG_GEODIRCOUNTRY4,pygeoip.MEMORY_CACHE)
        self.gi6 = pygeoip.GeoIP(settings.DBG_GEODIRCOUNTRY6,pygeoip.MEMORY_CACHE)
        self.giCity4 = pygeoip.GeoIP(settings.DBG_GEODIRCITY4,pygeoip.MEMORY_CACHE)
        self.count = 0
        
        