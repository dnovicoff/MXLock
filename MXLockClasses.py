"""
MXLock general functions file
"""

import time
import datetime
import random

class MXLockError(Exception):
    
    def __init__(self,value):
        self.value = value
        
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


