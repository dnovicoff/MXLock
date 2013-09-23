"""
File: domainWhois.py
Purpose: determine who owns an IP address
Copywrite: Sendwell 2013
"""

import sys
import whois
import whois.parser
import re

class DomainWhois(object):
    
    def writeError(self,message):
        if self.log is None:
            print "%s" % message
        else:
            self.log.writeLog(message)

    def getOwner(self):
        result = ""
        try:
            if self.lastRecord != "":
                if self.regEx['Registrant1'].search(self.lastRecord):
                    match = self.regEx['Registrant1'].search(self.lastRecord)
                    result = match.group(1)+"\n"+match.group(2)
                elif self.regEx['Registrant2'].search(self.lastRecord):
                    match = self.regEx['Registrant2'].search(self.lastRecord)
                    result = match.group(1)+"\n"+match.group(2)
                elif self.regEx['Registrant3'].search(self.lastRecord):
                    match = self.regEx['Registrant3'].search(self.lastRecord)
                    result = match.group(2)+"\n"+match.group(1)
                elif self.regEx['Registrant4'].search(self.lastRecord):
                    match = self.regEx['Registrant4'].search(self.lastRecord)
                    result = match.group(2)+"\n"+match.group(1)
                elif self.regEx['Registrant5'].search(self.lastRecord):
                    match = self.regEx['Registrant5'].search(self.lastRecord)
                    result = match.group(2)+"\n"+match.group(1)
                else:
                    result = "no match"
        except IndexError as e:
            message = "Error: getOwner error: %s %s" % (sys.exc_info()[0],e)
            self.writeError(message)
        return result
                
    def parseWhois(self,domain):
        result = whois.parser.WhoisEntry
        stuff = result.load(domain, self.lastRecord)
        print "%s\n\n\n%s" % (stuff,self.lastRecord)
        
    def getWhois(self,domain):
        result = ""
        try:
            result = whois.whois(domain)
            for (key,value) in result.__dict__.items():
                if key == "text":
                    self.lastRecord = value
        except:
            message = "Whois error: %s" % (sys.exc_info()[0])
            self.writeError(message)
        return result
        
    def setRegEx(self):
        self.regEx['Registrant1'] = re.compile('Registrant\sContact:\\n(.*)\\n(.*)\\n(.*)\\n(.*)\\n(.*)\\n(.*)\\n(.*)\\n(.*)\\n')
        self.regEx['Registrant2'] = re.compile('Registrant\s+Name:\s+(.*)\\n(.*)\\nRegistrant\s+Street')
        self.regEx['Registrant3'] = re.compile('Registrant:\\n(.*)\\n(.*)\\n')
        self.regEx['Registrant4'] = re.compile('Registrant\s+Name:\s+(.*)\\nRegistrant\s+Organization:\s+(.*)\\n')
        self.regEx['Registrant5'] = re.compile('Admin\s+Name...........\s+(.*)\\n.*Admin\s+Address........\s+(.*)\\n')
        
    def __init__(self,log=None):
        self.lastRecord = ""
        self.regEx = {}
        self.setRegEx()
        self.log = log
        
        