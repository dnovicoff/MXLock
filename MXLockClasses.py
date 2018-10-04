"""
MXLock general functions file
"""

import time
import datetime
import random
import DataConnect

class MXLockError(Exception):
    
    def __init__(self,value):
        self.value = value
        
def createTypes():
    select = "SELECT * FROM rtype"
    connect = DataConnect.DatabaseConnection()
    connect.startTransaction()
    results = connect.execQuery(select)
    connect.endCursor()
    types = {}
    for result in results:
        types[result[1]] = result[0]
    return types

def createGEOIPKeys():
    sql = "SELECT * FROM geo_city WHERE vcity='Placeholder'"
    connect = DataConnect.DatabaseConnection()
    connect.startTransaction()
    rows = connect.execQuery(sql)
    ph = {}
    if rows:
        for row in rows:
            ph['city'] = row[0]
            ph['country'] = row[1]
    else:
        sql = "INSERT INTO geo_country (vcountry,vcode) VALUES ('Placeholder','PH')"
        rows = connect.insertQuery(sql)
        sql = "SELECT id FROM geo_country WHERE vcountry='Placeholder'"
        rows = connect.getColumnInteger(sql)
        if rows:
            for row in rows:
                ph['country'] = row[0]
        sql = "INSERT INTO geo_city (ligeo_country_id,vcity,vstate,vzip,varea_code) VALUES (%s,'Placeholder','PH','00000','000')"
        rows = connect.insertQuery(sql)
        sql = "SELECT id FROM geo_city WHERE vcity='Placeholder'"
        rows = connect.getColumnInteger(sql)
        if rows:
            for row in rows:
                ph['city'] = row[0]
    connect.endCursor()
    return ph
        
def convertToEpoch(cTime):
    return (cTime - datetime.datetime(1970,1,1)).total_seconds()

def getNextCurPos(dct,curPos):
    newCurPos = 0
    if dct:
        if curPos+1 < dct.__len__():
            newCurPos = curPos+1
    return newCurPos

def writeLog(message,log=None):
    if log == None:
        print "%s" % message
    else:
        log.writeLog(message)

def getTimestamp():
    timestamp = int(round(time.time()))
    return timestamp

def getRandomNumber(start,finish):
    number = random.randint(start,finish)
    return number

def logName():
    localTime = time.localtime(time.time())
    return str(localTime[0])+"-"+str(localTime[1])+"-"+str(localTime[2])+"-"+str(localTime[3])+":"+str(localTime[4])+":"+str(localTime[5])+"_MXLock.log"


