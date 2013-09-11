"""
File: DataConnect.py
Purpose: Used to handle all database connections.
Copywrite: Sendwell 2013
"""
import MySQLdb as mdb
import psycopg2
import psycopg2.extras

import settings

class DatabaseConnection(object):
    
    def execQuery(self,query):
        rows = None
        try:
            if self.curs:
                self.curs.execute(query)
                rows = self.curs.fetchall()
        ## except mdb.Error as e:
        ##    print ("Database Select Error: %s" % e)
        except psycopg2.Error as ge:
            print "General error({0}): {1}".format(ge.args[0], ge.args[1])
        except psycopg2.InterfaceError as e:
            print "Interface error({0}): {1}".format(e.args[0], e.args[1])
        except psycopg2.DatabaseError as e:
            print "Database error({0}): {1}".format(e.args[0], e.args[1])
        except psycopg2.DataError as e:
            print "Data error({0}): {1}".format(e.args[0], e.args[1])
        except psycopg2.ProgrammingError as e:
            print "Programming error({0}): {1}".format(e.args[0], e.args[1])
        except psycopg2.InternalError as e:
            print "Internal error({0}): {1}".format(e.args[0], e.args[1])
        return rows
    
    def updateQuery(self,query):
        count = -1
        try:
            if self.curs:
                self.curs.execute(query)
                count = self.curs.rowcount
        ## except mdb.Error as e:
        ##    print ("Database Update Error: %s" % e)
        except psycopg2.Error as ge:
            print "General error({0}): {1}".format(ge.args[0], ge.args[1])
        except psycopg2.InterfaceError as e:
            print "Interface error({0}): {1}".format(e.args[0], e.args[1])
        except psycopg2.DatabaseError as e:
            print "Database error({0}): {1}".format(e.args[0], e.args[1])
        except psycopg2.DataError as e:
            print "Data error({0}): {1}".format(e.args[0], e.args[1])
        except psycopg2.ProgrammingError as e:
            print "Programming error({0}): {1}".format(e.args[0], e.args[1])
        except psycopg2.InternalError as e:
            print "Internal error({0}): {1}".format(e.args[0], e.args[1])
        return count
    
    def insertQuery(self,query):
        count = -1
        try:
            if self.curs:
                self.curs.execute(query)
                count = self.curs.rowcount
        ### except mdb.Error as e:
        ###    print ("Database Insert Error: %s" % e)
        except psycopg2.Error as ge:
            print "General error({0}): {1}".format(ge.args[0], ge.args[1])
        except psycopg2.InterfaceError as e:
            print "Interface error({0}): {1}".format(e.args[0], e.args[1])
        except psycopg2.DatabaseError as e:
            print "Database error({0}): {1}".format(e.args[0], e.args[1])
        except psycopg2.DataError as e:
            print "Data error({0}): {1}".format(e.args[0], e.args[1])
        except psycopg2.ProgrammingError as e:
            print "Programming error({0}): {1}".format(e.args[0], e.args[1])
        except psycopg2.InternalError as e:
            print "Internal error({0}): {1}".format(e.args[0], e.args[1])
        return count
    
    def getLastInsertID(self):
        uid = 0
        try:
            uid = self.conn.insert_id()
        ### except mdb.Error as e:
        ###    print("Database last insert ID error %s" % e)
        except psycopg2.Error as ge:
            print "General error({0}): {1}".format(ge.args[0], ge.args[1])
        except psycopg2.InterfaceError as e:
            print "Interface error({0}): {1}".format(e.args[0], e.args[1])
        except psycopg2.DatabaseError as e:
            print "Database error({0}): {1}".format(e.args[0], e.args[1])
        except psycopg2.DataError as e:
            print "Data error({0}): {1}".format(e.args[0], e.args[1])
        except psycopg2.ProgrammingError as e:
            print "Programming error({0}): {1}".format(e.args[0], e.args[1])
        except psycopg2.InternalError as e:
            print "Internal error({0}): {1}".format(e.args[0], e.args[1])
        return uid
    
    def autocommitTransaction(self):
        self.conn.autocommit()
        
    def commitTransaction(self):
        self.conn.commit()
    
    def rollbackTransaction(self):
        self.conn.rollback()
        
    def endCursor(self):
        self.curs = None
        
    def startTransaction(self):
        self.conn_string = "host='%s' dbname='%s' user='%s' password='%s'" % (settings.DBG_PGSQL_SERVER,settings.DBG_PGSQL_DATABASE,settings.DBG_PGSQL_USER,settings.DBG_PGSQL_PASS)
        self.conn = psycopg2.connect(self.conn_string)
        ### self.conn = mdb.connect(settings.DBG_PGSQL_SERVER,settings.DBG_PGSQL_USER,settings.DBG_PGSQL_PASS,settings.DBG_PGSQL_DATABASE)
        self.curs = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        ### self.curs = self.conn.cursor() 
    
    def __init__(self):
        self.database = "dns4new"
        
        