"""
File: DataConnect.py
Purpose: Used to handle all database connections.
Copywrite: Sendwell 2013
"""
import MySQLdb as mdb
import psycopg2
import psycopg2.extras

import settings
import MXLockClasses

class DatabaseConnection(object):
    
    def writeError(self,message):
        if self.log is None:
            print "%s" % message
        else:
            self.log.writeLog(message)
    
    def execQuery(self,query):
        message = ""
        rows = None
        try:
            if self.curs:
                self.curs.execute(query)
                rows = self.curs.fetchall()
        except psycopg2.Error as ge:
            message = "ExecQuery General error {0}".format(ge.args[0])[:-2]
        except psycopg2.InterfaceError as e:
            message = "Interface error {0}".format(e.args[0])
        except psycopg2.DatabaseError as e:
            message = "Database error {0}".format(e.args[0])
        except psycopg2.DataError as e:
            message = "Data error {0}".format(e.args[0])
        except psycopg2.ProgrammingError as e:
            message = "Programming error {0}".format(e.args[0])
        except psycopg2.InternalError as e:
            message = "Internal error {0}".format(e.args[0])
        finally:
            if message.__len__() > 1: 
                MXLockClasses.writeLog(message,self.log)
        return rows
    
    def updateQuery(self,query):
        message = ""
        count = -1
        try:
            if self.curs:
                self.curs.execute(query)
                count = self.curs.rowcount
        except psycopg2.Error as ge:
            message = "UpdateQuery General error {0}".format(ge.args[0])[:-2]
        except psycopg2.InterfaceError as e:
            message = "Interface error {0}".format(e.args[0])
        except psycopg2.DatabaseError as e:
            message = "Database error {0}".format(e.args[0])
        except psycopg2.DataError as e:
            message = "Data error {0}".format(e.args[0])
        except psycopg2.ProgrammingError as e:
            message = "Programming error {0}".format(e.args[0])
        except psycopg2.InternalError as e:
            message = "Internal error {0}".format(e.args[0])
        finally:
            if message.__len__() > 1:
                MXLockClasses.writeLog(message,self.log)
        return count
    
    def insertQuery(self,query):
        message = ""
        count = -1
        try:
            if self.curs:
                self.curs.execute(query)
                count = self.curs.rowcount
        except psycopg2.Error as ge:
            message = "InseretQuery General error({0}) ({1})".format(ge.args[0],query)
        except psycopg2.InterfaceError as e:
            message = "Interface error({0})".format(e.args[0])
        except psycopg2.DatabaseError as e:
            message = "Database error({0})".format(e.args[0])
        except psycopg2.DataError as e:
            message = "Data error({0})".format(e.args[0])
        except psycopg2.ProgrammingError as e:
            message = "Programming error({0})".format(e.args[0])
        except psycopg2.InternalError as e:
            message = "Internal error({0})".format(e.args[0])
        finally:
            if message.__len__() > 1:
                MXLockClasses.writeLog(message,self.log)
        return count
    
    def getColumnInteger(self,query):
        message = ""
        uid = 0
        try:
            if self.curs:
                self.curs.execute(query)
                rows = self.curs.fetchall()
                if rows:
                    for row in rows:
                        uid = row[0]
        except psycopg2.Error as ge:
            message = "GetColumnInteger General error({0})".format(ge.args[0],query)
        except psycopg2.InterfaceError as e:
            message = "Interface error({0})".format(e.args[0])
        except psycopg2.DatabaseError as e:
            message = "Database error({0})".format(e.args[0])
        except psycopg2.DataError as e:
            message = "Data error({0})".format(e.args[0])
        except psycopg2.ProgrammingError as e:
            message = "Programming error({0})".format(e.args[0])
        except psycopg2.InternalError as e:
            message = "Internal error({0})".format(e.args[0])
        finally:
            if message.__len__() > 1:
                MXLockClasses.writeLog(message,self.log)
        return int(uid)
    
    def autocommitTransaction(self):
        if self.conn:
            self.conn.autocommit()
        
    def commitTransaction(self):
        if self.conn:
            self.conn.commit()
    
    def rollbackTransaction(self):
        if self.conn:
            self.conn.rollback()
        
    def endCursor(self):
        if self.curs:
            self.curs = None
        
    def startTransaction(self):
        self.conn_string = "host='%s' dbname='%s' user='%s' password='%s'" % (settings.DBG_PGSQL_SERVER,settings.DBG_PGSQL_DATABASE,settings.DBG_PGSQL_USER,settings.DBG_PGSQL_PASS)
        self.conn = psycopg2.connect(self.conn_string)
        ### self.conn = mdb.connect(settings.DBG_PGSQL_SERVER,settings.DBG_PGSQL_USER,settings.DBG_PGSQL_PASS,settings.DBG_PGSQL_DATABASE)
        self.curs = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        ### self.curs = self.conn.cursor() 
    
    def __init__(self,log=None):
        self.database = "dns4new"
        self.log = log
        
        