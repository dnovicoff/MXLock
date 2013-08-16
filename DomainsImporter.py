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
        conn = mdb.connect(settings.DBG_PGSQL_SERVER,settings.DBG_PGSQL_USER,settings.DBG_PGSQL_PASS,settings.DBG_PGSQL_DATABASE)
        curs = conn.cursor()
        
        curs.execute("SET autocommit = 0")
        for domain in domainNames:
            sqlReplace = "REPLACE INTO soa (origin) VALUES ('%s')" % domain
            ## sqlReplace = "INSERT INTO soa (domain) VALUES ('%s') ON DUPLICATE KEY UPDATE domain = '%s'" % (domain,domain)
            curs.execute(sqlReplace)
            
        curs.execute("SET autocommit = 1")
        curs.close()
        conn.close()
            
    def __init__(self):
        self.count = 0
        