"""
File: DataConnect.py
Purpose: Used to handle all database connections.
Copywrite: Sendwell 2013
"""
import MySQLdb as mdb
import threading

import settings

class DatabaseConnection(object):
    
    def execQuery(self,query):
        rows = None
        try:
            if self.curs:
                self.curs.execute(query)
                rows = self.curs.fetchall()
        except mdb.Error as e:
            print ("Database Select Error: %s" % e)
        return rows
    
    def updateQuery(self,query):
        count = -1
        try:
            if self.curs:
                self.curs.execute(query)
                count = self.curs.rowcount
        except mdb.Error as e:
            print ("Database Update Error: %s" % e)
        return count
    
    def insertQuery(self,query):
        count = -1
        try:
            if self.curs:
                self.curs.execute(query)
                count = self.curs.rowcount
        except mdb.Error as e:
            print ("Database Insert Error: %s" % e)
        return count
    
    def getLastInsertID(self):
        uid = 0
        try:
            uid = self.conn.insert_id()
        except mdb.Error as e:
            print("Database last insert ID error %s" % e)
        return uid
    
    def autocommitTransaction(self):
        self.conn.autocommit(1)
        
    def commitTransaction(self):
        self.conn.commit()
    
    def rollbackTransaction(self):
        self.conn.rollback()
        
    def endCursor(self):
        self.curs = None
        
    def startTransaction(self):
        self.conn = mdb.connect(settings.DBG_PGSQL_SERVER,settings.DBG_PGSQL_USER,settings.DBG_PGSQL_PASS,settings.DBG_PGSQL_DATABASE)
        self.curs = self.conn.cursor() 
    
    def __init__(self):
        self.database = "mysql"
        #self.conn.autocommit(1)
        
        