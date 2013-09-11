"""
MXLock general functions file
"""

import time
import random

def getTimestamp():
    timestamp = int(round(time.time()))
    return timestamp

def getRandomNumber(start,finish):
    number = random.randint(start,finish)
    return number

def logName():
    localTime = time.localtime(time.time())
    return str(localTime[0])+"-"+str(localTime[1])+"-"+str(localTime[2])+"-"+str(localTime[3])+":"+str(localTime[4])+":"+str(localTime[5])+"_MXLock.log"


