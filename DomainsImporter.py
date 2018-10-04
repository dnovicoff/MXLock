"""
File: DomainsImporter.py
Purpose: Used as a seed to the database
CopyWrite: Sendwell 2013
"""

import psycopg2
import psycopg2.extras
import MySQLdb as mdb

import settings

class DomainsImporter(object):
    
    def addDomains(self,domainNames):
        print ("Adding Domains: ")
        self.conn_string = "host='%s' dbname='%s' user='%s' password='%s'" % (settings.DBG_PGSQL_SERVER,settings.DBG_PGSQL_DATABASE,settings.DBG_PGSQL_USER,settings.DBG_PGSQL_PASS)
        self.conn = psycopg2.connect(self.conn_string)
        self.curs = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        #conn = mdb.connect(settings.DBG_PGSQL_SERVER,settings.DBG_PGSQL_USER,settings.DBG_PGSQL_PASS,settings.DBG_PGSQL_DATABASE)
        #curs = conn.cursor()
        
        self.conn.autocommit = True
        for domain in domainNames:
            sqlReplace = "INSERT INTO soa (vorigin) VALUES ('%s')" % domain
            ## sqlReplace = "INSERT INTO soa (domain) VALUES ('%s') ON DUPLICATE KEY UPDATE domain = '%s'" % (domain,domain)
            self.curs.execute(sqlReplace)
            
        self.curs.close()
        self.conn.close()
            
    def __init__(self):
        self.count = 0
        