"""
File: logger.py
Purpose: provide an interface for writing log files
Copywrite: 2013 Sendwell Inc.
"""

import settings

import logging

class logger(object):
    
    def writeLog(self,data):
        self.logger.info(data)
    
    def __init__(self,logName):
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                            datefmt='%m-%d %H:%M',
                            filename=settings.GEN_LOG_PATH+"/"+logName,
                            filemode='w')
        self.logger = logging.getLogger("MXLock Logger")
        