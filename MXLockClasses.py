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


